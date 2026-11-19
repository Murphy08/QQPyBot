"""QQ REST API 客户端，缓存访问凭证，并对请求错误暴露业务码。"""

import asyncio
import json
import string
import time
from importlib.resources import files
from urllib.error import HTTPError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

CATALOG = json.loads(files(__package__).joinpath("catalog.json").read_text(encoding="utf-8"))


class QQAPIError(RuntimeError):
    """QQ REST 接口拒绝请求时返回的状态码、业务码与 Trace ID。"""

    def __init__(self, status: int, code, trace_id: str | None):
        self.status, self.code, self.trace_id = status, code, trace_id
        super().__init__(f"QQ API returned HTTP {status}, code={code}, trace_id={trace_id}")


class _NoRedirect(HTTPRedirectHandler):
    """避免将 QQ 鉴权头转发到重定向目标。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class QQClient:
    """使用 QQBot Access Token 调用官方群、私聊和频道接口。"""

    def __init__(self, app_id: str, app_secret: str, *, sandbox=False, timeout=10):
        if not app_id or not app_secret:
            raise ValueError("QQ App ID and App Secret are required")
        self.app_id = app_id
        self._secret = app_secret
        self._timeout = timeout
        self._base = "https://sandbox.api.sgroup.qq.com" if sandbox else "https://api.sgroup.qq.com"
        self._token = ""
        self._expires = 0.0
        self._token_lock = asyncio.Lock()
        self._opener = build_opener(_NoRedirect())

    def _send(self, target, method, body, headers):
        """在线程中发送 HTTP 请求，并保留 QQ 错误的诊断元数据。"""
        request = Request(target, data=body, headers=headers, method=method)
        try:
            with self._opener.open(request, timeout=self._timeout) as response:
                data = response.read()
                return json.loads(data) if data else None
        except HTTPError as error:
            with error:
                try:
                    content = json.loads(error.read())
                except (ValueError, UnicodeError):
                    content = {}
                code = content.get("code") if isinstance(content, dict) else None
                raise QQAPIError(error.code, code, error.headers.get("X-Tps-Trace-ID")) from None

    async def access_token(self) -> str:
        """获取或复用访问凭证，并在接近过期时自动刷新。"""
        async with self._token_lock:
            if time.monotonic() < self._expires:
                return self._token
            result = await asyncio.to_thread(
                self._send, "https://bots.qq.com/app/getAppAccessToken", "POST",
                json.dumps({"appId": self.app_id, "clientSecret": self._secret}).encode(),
                {"Content-Type": "application/json"},
            )
            if not isinstance(result, dict) or not isinstance(result.get("access_token"), str):
                raise QQAPIError(200, result.get("code") if isinstance(result, dict) else None, None)
            self._token = result["access_token"]
            self._expires = time.monotonic() + max(0, int(result["expires_in"]) - 30)
            return self._token

    async def request(self, method: str, path: str, *, query=None, json_body=None):
        """调用相对路径的 QQ API，可用于上线后新增的接口。"""
        parts = urlsplit(path)
        if not path.startswith("/") or path.startswith("//") or parts.netloc or parts.fragment or parts.query:
            raise ValueError("Expected an API path without origin, query or fragment")
        token = await self.access_token()
        headers = {"Authorization": f"QQBot {token}", "X-Union-Appid": self.app_id}
        body = None
        if json_body is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(json_body, ensure_ascii=False).encode()
        suffix = "?" + urlencode(query, doseq=True) if query else ""
        return await asyncio.to_thread(self._send, self._base + path + suffix, method.upper(), body, headers)

    async def call(self, name: str, *, query=None, json_body=None, **path_parameters):
        """通过官方接口目录名称调用 REST API，并编码每个路径参数。"""
        api = CATALOG["apis"][name]
        expected = {field for _, field, _, _ in string.Formatter().parse(api["path"]) if field}
        if expected != path_parameters.keys():
            raise ValueError(f"{name} requires path parameters {', '.join(sorted(expected))}")
        path = api["path"].format_map({key: quote(str(value), safe="") for key, value in path_parameters.items()})
        return await self.request(api["method"], path, query=query, json_body=json_body)

    async def send_group_message(self, group_openid: str, **payload):
        """向 QQ 群主动发送或被动回复一条消息。"""
        return await self.request("POST", f"/v2/groups/{quote(group_openid, safe='')}/messages", json_body=payload)

    async def upload_group_file(self, group_openid: str, **payload):
        """上传 QQ 群富媒体，返回供发送接口使用的 file_info。"""
        return await self.request("POST", f"/v2/groups/{quote(group_openid, safe='')}/files", json_body=payload)
