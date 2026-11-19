"""在控制台观察 QQ 官方目录中的每一种事件。"""

import os

from qqpybot import Bot, CATALOG, Context

bot = Bot(os.environ["QQBOT_APP_ID"], os.environ["QQBOT_APP_SECRET"])


async def report(ctx: Context):
    """显示收到的事件类型和 ID。"""
    print(ctx.event.type, ctx.event.event_id)


for event_name in CATALOG["events"]:
    bot.on_event(event_name)(report)


@bot.command("你好", aliases=("hi",))
async def hello(ctx: Context):
    """回复普通群消息或 @ 中的命令。"""
    await ctx.reply(f"你好，{ctx.args or '朋友'}！")


app = bot.create_app()
