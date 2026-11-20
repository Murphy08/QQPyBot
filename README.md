# QQPyBot

[![CI](https://github.com/Murphy08/QQPyBot/actions/workflows/ci.yml/badge.svg)](https://github.com/Murphy08/QQPyBot/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/QQPyBot)](https://pypi.org/project/QQPyBot/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![GitHub Stars](https://img.shields.io/github/stars/Murphy08/QQPyBot?style=social)](https://github.com/Murphy08/QQPyBot/stargazers)

QQ 开放平台的 Python **Webhook SDK**。用 FastAPI 接收 QQ 事件，使用装饰器注册命令，并通过异步客户端调用 QQ REST API。

## 快速开始

PyPI 首发完成后，使用 `pip install QQPyBot uvicorn`。也可以克隆本仓库后运行 `python -m pip install -e . uvicorn`。运行环境需要 Python 3.11 以上及提供 Ed25519 的 OpenSSL。Windows 版 CPython 可使用自带的 OpenSSL。

把下面的示例保存为 `main.py`。

```python
import os

from qqpybot import Bot, Context

bot = Bot(os.environ["QQBOT_APP_ID"], os.environ["QQBOT_APP_SECRET"])

@bot.command("你好", aliases=("hi",), events={"GROUP_MESSAGE_CREATE", "GROUP_AT_MESSAGE_CREATE"})
async def hello(ctx: Context):
    await ctx.reply(f"你好，{ctx.args or '朋友'}！")

app = bot.create_app()
```

执行 `python -m uvicorn main:app --host 0.0.0.0 --port 8080`。在 QQ 开放平台填写对外的 HTTPS 回调地址 `https://你的域名/qq/callback`。可在已有 FastAPI 中使用 `app.include_router(bot.router)`。

勾选 `GROUP_MESSAGE_CREATE` 并为机器人启用接收所有消息。群里直接发送 `你好 小明` 或 `/hi 小明`。只订阅 AT 事件的群，用 `@机器人 你好 小明`。QQ 平台管理的账号注册、事件订阅、权限和回调地址配置请参阅[官方接入指南](https://bot.q.qq.com/wiki/develop/api-v2/dev-prepare/getting-started.html)。

## 事件与 REST

```python
@bot.on_event("GROUP_ADD_ROBOT")
async def joined(ctx: Context):
    print("已加入群聊", ctx.event.group_openid)

@bot.on_event("*")
async def delivered(ctx: Context):
    print(ctx.event.type, ctx.event.event_id)
```

[全事件示例](docs/events.md)包含逐项订阅的调用方式。也可运行 `uvicorn examples.all_events:app` 观察官方回调。事件数据通过 `ctx.event.data` 取得。

```python
await bot.api.send_group_message("群 OpenID", msg_type=0, content="晚上好")
await bot.api.call("v2_groups_group_openid_info_get", group_openid="群 OpenID")
await bot.api.request("GET", "/users/@me")
```

[REST 目录](docs/api.md)列出官网自动生成的接口及参数示例。登录凭证由 SDK 缓存，API 失败时可从 `QQAPIError` 读取 HTTP 状态、业务码和 Trace ID。管理、主动消息及其他受限接口取决于应用权限。

回调会先验签、应答 QQ，随后在当前进程执行已注册的处理器。同一进程内会过滤近期重复事件。需要跨进程去重或可靠重放的业务，应在业务层持久化事件 ID。

## 开发与发布

在项目的虚拟环境运行 `python -m pip install -e .`，然后执行 `python -m unittest discover -s tests -v`。更新接口或事件时，维护 `src/qqpybot/catalog.json` 并运行 `python scripts/build_docs.py` 更新对应文档。

发布前在 PyPI 建立 Trusted Publisher，项目名填 `QQPyBot`，GitHub Owner 填 `Murphy08`，仓库填 `QQPyBot`，工作流填 `publish.yml`，环境填 `pypi`。更新 `pyproject.toml` 中的版本，推送对应 `vX.Y.Z` 标签即可构建并发布。
