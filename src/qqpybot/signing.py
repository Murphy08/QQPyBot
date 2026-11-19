"""通过系统 OpenSSL EVP 接口完成 QQ Webhook 的 Ed25519 签名。"""

import ctypes as c
import ctypes.util
import re
import ssl
import sys
from pathlib import Path


def _load_crypto():
    """在 Windows 上选择 Python 自带的 DLL，在其他平台上使用系统 libcrypto。"""
    candidates = []
    if sys.platform == "win32":
        for root in (Path(sys.base_prefix), Path(sys.base_prefix) / "DLLs"):
            candidates.extend(str(p) for p in sorted(root.glob("libcrypto-*.dll")))
    name = ctypes.util.find_library("crypto")
    if name:
        candidates.append(name)
    for candidate in candidates:
        try:
            lib = c.CDLL(candidate)
            if hasattr(lib, "EVP_PKEY_new_raw_private_key"):
                return lib
        except OSError:
            continue
    raise RuntimeError(f"QQPyBot requires OpenSSL with Ed25519 (Python SSL: {ssl.OPENSSL_VERSION})")


class WebhookSigner:
    """按 QQ 官方规则派生 Ed25519 密钥，验证请求及签署回调挑战。"""

    def __init__(self, secret: str):
        raw = secret.encode("utf-8")
        if not raw:
            raise ValueError("QQ App Secret is required")
        self._seed = (raw * ((32 + len(raw) - 1) // len(raw)))[:32]
        self._crypto = _load_crypto()
        pointer, data, size = c.c_void_p, c.c_char_p, c.c_size_t
        for name, result, args in (
            ("OBJ_txt2nid", c.c_int, [data]),
            ("EVP_PKEY_new_raw_private_key", pointer, [c.c_int, pointer, data, size]),
            ("EVP_PKEY_free", None, [pointer]),
            ("EVP_MD_CTX_new", pointer, []),
            ("EVP_MD_CTX_free", None, [pointer]),
            ("EVP_DigestSignInit", c.c_int, [pointer, pointer, pointer, pointer, pointer]),
            ("EVP_DigestVerifyInit", c.c_int, [pointer, pointer, pointer, pointer, pointer]),
            ("EVP_DigestSign", c.c_int, [pointer, pointer, c.POINTER(size), data, size]),
            ("EVP_DigestVerify", c.c_int, [pointer, data, size, data, size]),
        ):
            func = getattr(self._crypto, name)
            func.restype, func.argtypes = result, args
        self._nid = self._crypto.OBJ_txt2nid(b"ED25519")
        if not self._nid:
            raise RuntimeError("OpenSSL does not expose Ed25519")

    def sign(self, message: bytes) -> str:
        """返回十六进制 Ed25519 签名。"""
        return self._operate(message).hex()

    def verify(self, message: bytes, signature: str) -> bool:
        """验证十六进制 Ed25519 签名，并拒绝格式错误的输入。"""
        return bool(re.fullmatch(r"[0-9a-fA-F]{128}", signature)) and self._operate(
            message, bytes.fromhex(signature)
        )

    def _operate(self, message: bytes, signature: bytes | None = None):
        """使用每次调用独立的 EVP 上下文，确保多线程中可以复用签名器。"""
        lib = self._crypto
        key = lib.EVP_PKEY_new_raw_private_key(self._nid, None, self._seed, len(self._seed))
        ctx = lib.EVP_MD_CTX_new()
        try:
            if not key or not ctx:
                raise RuntimeError("OpenSSL cannot initialize Ed25519")
            if signature is not None:
                if lib.EVP_DigestVerifyInit(ctx, None, None, None, key) != 1:
                    raise RuntimeError("OpenSSL cannot initialize signature verification")
                return lib.EVP_DigestVerify(ctx, signature, len(signature), message, len(message)) == 1
            if lib.EVP_DigestSignInit(ctx, None, None, None, key) != 1:
                raise RuntimeError("OpenSSL cannot initialize signing")
            output = c.create_string_buffer(64)
            size = c.c_size_t(64)
            if lib.EVP_DigestSign(ctx, output, c.byref(size), message, len(message)) != 1:
                raise RuntimeError("OpenSSL cannot sign the QQ callback")
            return output.raw[:size.value]
        finally:
            lib.EVP_MD_CTX_free(ctx)
            lib.EVP_PKEY_free(key)
