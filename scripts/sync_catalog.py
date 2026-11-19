"""从 QQ 官方 sitemap 同步生成接口与事件索引。"""

import concurrent.futures
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import urlopen

SITEMAP = "https://bot.q.qq.com/wiki/sitemap.xml"
ROOT = Path(__file__).resolve().parents[1]


def read(url):
    """读取官方文档页面。"""
    with urlopen(url, timeout=15) as response:
        return response.read()


def plain(markup):
    """将表格单元格转换成纯文本。"""
    return html.unescape(re.sub(r"<[^>]+>", "", markup)).strip()


def entry(url):
    """提取接口方法、路径或事件名称。"""
    raw = read(url).decode()
    title = plain(re.search(r"<title>(.*?)\s*\|", raw).group(1))
    rows = {
        plain(left): plain(right)
        for left, right in re.findall(r"<tr>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>", raw, re.S)
    }
    if "/autogen/api/" in url:
        method = rows.get("HTTP Method")
        path = next((value for value in rows.values() if value.startswith("/")), None)
        if not method or not path:
            raise ValueError("Missing method or route in " + url)
        name = url.rsplit("/", 1)[-1].removesuffix(".html").replace(".", "_")
        return "apis", name, {"method": method, "path": path, "title": title, "doc": url}
    name = rows.get("事件名") or rows.get("事件类型")
    if not name or not re.fullmatch(r"[A-Z][A-Z0-9_]+", name):
        raise ValueError("Missing event name in " + url)
    return "events", name, {"title": title, "doc": url}


def main():
    """写入随 wheel 一起发布的接口与事件索引。"""
    sitemap = ET.fromstring(read(SITEMAP))
    links = [
        node.text for node in sitemap.findall(".//{*}loc") if "/api-v2/autogen/" in (node.text or "")
        and re.search(r"/autogen/(api|event)/[^/]+\.html$", node.text)
    ]
    catalog = {"apis": {}, "events": {}}
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(entry, url): url for url in links}
        for result in concurrent.futures.as_completed(futures):
            try:
                category, name, metadata = result.result()
                catalog[category][name] = metadata
            except Exception as error:
                failures.append(str(error))
    for failure in failures:
        print(failure)
    target = ROOT / "src" / "qqpybot" / "catalog.json"
    target.write_text(json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print({name: len(items) for name, items in catalog.items()})


if __name__ == "__main__":
    main()
