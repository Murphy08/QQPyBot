"""测试官方签名示例和通过 FastAPI 分发的免 @ 命令。"""

import json
import time
import unittest

from qqpybot import Bot, CATALOG
from qqpybot.signing import WebhookSigner


class WebhookTest(unittest.IsolatedAsyncioTestCase):
    def test_qq_signature_example(self):
        signer = WebhookSigner("DG5g3B4j9X2KOErG")
        message = b"1725442341Arq0D5A61EgUu4OxUvOp"
        expected = ("87befc99c42c651b3aac0278e71ada338433ae26fcb24307bdc5ad38c1adc2d01bcf"
                    "cadc0842edac85e85205028a1132afe09280305f13aa6909ffc2d652c706")
        self.assertEqual(signer.sign(message), expected)
        self.assertTrue(signer.verify(message, expected))
        self.assertFalse(signer.verify(message + b"x", expected))

    async def test_signed_event_dispatch_and_reject_tampering(self):
        bot = Bot("app-id", "demo-secret")
        calls = []

        @bot.command("活动日历")
        async def calendar(ctx):
            calls.append(ctx.args)

        payload = {"op": 0, "t": "GROUP_MESSAGE_CREATE", "id": "event-id",
                   "d": {"id": "message-id", "group_openid": "group", "content": "活动日历 2026-11"}}
        body = json.dumps(payload, ensure_ascii=False).encode()
        timestamp = str(int(time.time())).encode()
        signature = bot.signer.sign(timestamp + body).encode()
        app = bot.create_app()

        async def post(content):
            responses = []

            async def receive():
                return {"type": "http.request", "body": content, "more_body": False}

            async def send(message):
                responses.append(message)

            await app({
                "type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
                "method": "POST", "scheme": "https", "path": "/qq/callback",
                "root_path": "", "query_string": b"",
                "headers": [(b"x-bot-appid", b"app-id"), (b"x-signature-timestamp", timestamp),
                            (b"x-signature-ed25519", signature)],
            }, receive, send)
            return responses[0]["status"], json.loads(responses[1]["body"])

        self.assertEqual(await post(body + b" "), (401, {"detail": "Invalid QQ signature"}))
        self.assertEqual(await post(body), (200, {"op": 12}))
        self.assertEqual(await post(body), (200, {"op": 12}))
        self.assertEqual(calls, ["2026-11"])
        self.assertIn("GROUP_MESSAGE_CREATE", CATALOG["events"])
