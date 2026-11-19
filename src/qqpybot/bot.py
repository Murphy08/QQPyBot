"""FastAPI 回调、事件分发和命令装饰器。"""

import asyncio
import json
import logging
import re
import time
from collections import OrderedDict
from dataclasses import dataclass

from fastapi import APIRouter, BackgroundTasks, FastAPI, HTTPException, Request
from starlette.requests import ClientDisconnect

from .client import QQClient
from .signing import WebhookSigner

LOGGER = logging.getLogger("qqpybot")
MESSAGE_EVENTS = {
    "GROUP_MESSAGE_CREATE", "GROUP_AT_MESSAGE_CREATE", "C2C_MESSAGE_CREATE",
    "AT_MESSAGE_CREATE", "MESSAGE_CREATE", "DIRECT_MESSAGE_CREATE",
}


@dataclass(frozen=True)
class Event:
    """保留官方事件名、事件 ID 和完整业务载荷。"""

    type: str
    data: dict
    event_id: str | None = None

    @property
    def message_id(self) -> str | None:
        return self.data.get("id")

    @property
    def group_openid(self) -> str | None:
        return self.data.get("group_openid")

    @property
    def content(self) -> str:
        content = self.data.get("content")
        return content if isinstance(content, str) else ""


@dataclass(frozen=True)
class Context:
    """事件处理上下文和被动回复助手。"""

    event: Event
    api: QQClient
    args: str = ""

    async def reply(self, content: str):
        """回复群聊、单聊、频道或频道私信。"""
        event = self.event
        data = event.data
        if not event.message_id:
            raise ValueError("Event has no message ID")
        if event.group_openid:
            return await self.api.send_group_message(
                event.group_openid, content=content, msg_id=event.message_id, msg_type=0,
            )
        if event.type == "C2C_MESSAGE_CREATE":
            from urllib.parse import quote
            user = data["author"]["user_openid"]
            return await self.api.request(
                "POST", f"/v2/users/{quote(user, safe='')}/messages",
                json_body={"content": content, "msg_id": event.message_id, "msg_type": 0},
            )
        from urllib.parse import quote
        if event.type == "DIRECT_MESSAGE_CREATE":
            path = f"/dms/{quote(data['guild_id'], safe='')}/messages"
        elif event.type in {"AT_MESSAGE_CREATE", "MESSAGE_CREATE"}:
            path = f"/channels/{quote(data['channel_id'], safe='')}/messages"
        else:
            raise ValueError("Event does not support a text reply")
        return await self.api.request("POST", path, json_body={"content": content, "msg_id": event.message_id})


class Bot:
    """在 FastAPI 中接收 QQ 官方回调并注册异步事件和命令。"""

    def __init__(
        self, app_id: str, app_secret: str, *, path: str = "/qq/callback",
        sandbox=False, max_body_bytes=1024 * 1024, max_clock_skew=300,
    ):
        self.api = QQClient(app_id, app_secret, sandbox=sandbox)
        self.signer = WebhookSigner(app_secret)
        self.router = APIRouter()
        self.router.add_api_route(path, self._receive, methods=["POST"], include_in_schema=False)
        self._app_id = app_id
        self._max_body_bytes = max_body_bytes
        self._max_clock_skew = max_clock_skew
        self._handlers = {}
        self._commands = {}
        self._seen = OrderedDict()
        self._slots = asyncio.Semaphore(16)

    def create_app(self, **kwargs) -> FastAPI:
        """构建独立应用，或用 router 挂载到已有 FastAPI 服务。"""
        app = FastAPI(**kwargs)
        app.include_router(self.router)
        return app

    def on_event(self, name: str = "*"):
        """注册任意官方事件，使用 * 监听全部已订阅事件。"""
        def register(handler):
            self._handlers.setdefault(name.upper(), []).append(handler)
            return handler
        return register

    def command(self, name: str, *, aliases=(), events=None):
        """注册命令及别名，支持可选斜杠前缀和原始参数文本。"""
        event_types = MESSAGE_EVENTS if events is None else frozenset(events)
        def register(handler):
            names = (name, *aliases)
            if any(not value or value.startswith("/") or any(c.isspace() for c in value) for value in names):
                raise ValueError("Command names must be nonempty words")
            if any(value in self._commands for value in names):
                raise ValueError("Command name or alias is already registered")
            for value in names:
                self._commands[value] = (event_types, handler)
            return handler
        return register

    async def dispatch(self, event: Event):
        """分发已验证的事件，并对命令执行去重。"""
        async with self._slots:
            context = Context(event, self.api)
            for handler in (*self._handlers.get("*", ()), *self._handlers.get(event.type, ())):
                await self._invoke(handler, context)
            content = event.content.strip()
            if event.type in {"GROUP_AT_MESSAGE_CREATE", "AT_MESSAGE_CREATE"}:
                content = re.sub(r"^<@!?[A-Za-z0-9_-]+>\s*", "", content)
            parts = content.removeprefix("/").split(maxsplit=1)
            if event.type not in MESSAGE_EVENTS or not parts or parts[0] not in self._commands:
                return
            events, handler = self._commands[parts[0]]
            if event.type not in events or self._duplicate(("command", event.group_openid, event.message_id)):
                return
            await self._invoke(handler, Context(event, self.api, parts[1] if len(parts) == 2 else ""))

    async def _invoke(self, handler, context):
        """记录处理错误，同时保持同一事件的其他处理器可继续运行。"""
        try:
            await handler(context)
        except Exception as error:
            LOGGER.error(
                "QQ event handler failed event=%s handler=%s error=%s",
                context.event.type, getattr(handler, "__name__", type(handler).__name__), type(error).__name__,
            )

    def _duplicate(self, key):
        """用有限容量和生存期拦截同一进程内重复投递。"""
        if not key[-1]:
            return False
        now = time.monotonic()
        while self._seen and next(iter(self._seen.values())) < now - 600:
            self._seen.popitem(last=False)
        if key in self._seen:
            return True
        self._seen[key] = now
        if len(self._seen) > 4096:
            self._seen.popitem(last=False)
        return False

    async def _receive(self, request: Request, background: BackgroundTasks):
        """验证 QQ 请求，快速应答，并在应答后分发业务事件。"""
        if request.headers.get("X-Bot-Appid") != self._app_id:
            raise HTTPException(401, "Invalid bot App ID")
        body = bytearray()
        try:
            async for chunk in request.stream():
                if len(body) + len(chunk) > self._max_body_bytes:
                    raise HTTPException(413, "QQ callback is too large")
                body.extend(chunk)
        except ClientDisconnect as error:
            raise HTTPException(400, "QQ callback disconnected") from error
        try:
            payload = json.loads(body)
        except (ValueError, RecursionError) as error:
            raise HTTPException(400, "Invalid QQ callback JSON") from error
        if not isinstance(payload, dict) or not isinstance(payload.get("d"), dict):
            raise HTTPException(400, "Invalid QQ callback payload")
        data = payload["d"]
        if payload.get("op") == 13:
            timestamp, token = data.get("event_ts"), data.get("plain_token")
            if not isinstance(timestamp, str) or not re.fullmatch(r"[0-9]{1,16}", timestamp):
                raise HTTPException(400, "Invalid challenge timestamp")
            if not isinstance(token, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,256}", token):
                raise HTTPException(400, "Invalid challenge token")
            return {"plain_token": token, "signature": self.signer.sign((timestamp + token).encode())}

        timestamp = request.headers.get("X-Signature-Timestamp", "")
        signature = request.headers.get("X-Signature-Ed25519", "")
        if not re.fullmatch(r"[0-9]{1,12}", timestamp) or abs(time.time() - int(timestamp)) > self._max_clock_skew:
            raise HTTPException(401, "Invalid QQ signature timestamp")
        if not self.signer.verify(timestamp.encode() + body, signature):
            raise HTTPException(401, "Invalid QQ signature")
        name = payload.get("t")
        if payload.get("op") != 0 or not isinstance(name, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]{1,128}", name):
            raise HTTPException(400, "Invalid QQ event")
        event_id = payload.get("id")
        if not isinstance(event_id, str):
            event_id = None
        if not self._duplicate(("delivery", name, event_id)):
            background.add_task(self.dispatch, Event(name, data, event_id))
        return {"op": 12}
