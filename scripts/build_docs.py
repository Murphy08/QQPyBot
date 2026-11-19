"""根据 SDK 目录生成事件和 REST 接口调用示例。"""

import json
import string
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = json.loads((ROOT / "src/qqpybot/catalog.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)

events = ["# 事件订阅示例", "", "以下示例假定已有 `bot = Bot(app_id, app_secret)`。需要在 QQ 开放平台勾选对应事件。", ""]
for name, entry in INDEX["events"].items():
    events.extend([
        f"## {entry['title']}", "", f"[官方字段说明]({entry['doc']})", "", "```python",
        f'@bot.on_event("{name}")', f"async def on_{name.lower()}(ctx):",
        '    print(ctx.event.type, ctx.event.event_id)', "```", "",
    ])
apis = ["# REST 接口目录", "", "每个调用均支持 `query` 和 `json_body` 参数。按官方说明填写请求体。", ""]
for name, entry in INDEX["apis"].items():
    args = [f"{field}='你的 {field}'" for _, field, _, _ in string.Formatter().parse(entry["path"]) if field]
    method = entry["method"].upper()
    if method in {"POST", "PATCH", "PUT"}:
        args.append("json_body=body")
    call = f"await bot.api.call({', '.join([repr(name), *args])})"
    apis.extend([
        f"## {entry['title']}", "", f"`{method} {entry['path']}`", "",
        f"[官方请求和响应字段]({entry['doc']})", "", "```python", call, "```", "",
    ])
for name, lines in (("events.md", events), ("api.md", apis)):
    (OUT / name).write_text("\n".join(lines), encoding="utf-8")
