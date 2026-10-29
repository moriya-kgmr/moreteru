"""国内セキュリティニュースのRSSから、情報漏洩に関する記事の見出しを集めて news.json に保存する。

GitHub Actions（.github/workflows/update-news.yml）から1時間ごとに実行される。
保存するのは見出し・リンク・日時・配信元名だけで、記事本文は保存しない。
"""
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEEDS = [
    ("Security NEXT", "https://www.security-next.com/feed"),
    ("ScanNetSecurity", "https://scan.netsecurity.ne.jp/rss/index.rdf"),
]
KEYWORDS = re.compile(r"流出|漏洩|漏えい|個人情報|不正アクセス|ランサム|サイバー攻撃|侵害|誤送信|閲覧可能")
MAX_ITEMS = 10


def parse_date(text):
    text = (text or "").strip()
    try:
        return parsedate_to_datetime(text).astimezone(timezone.utc)
    except Exception:
        pass
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def load(name, url):
    req = urllib.request.Request(url, headers={"User-Agent": "moreteru-news/1.0 (+https://moreteru.com)"})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
    items = []
    for node in root.iter():
        if node.tag.split("}")[-1] != "item":
            continue
        fields = {child.tag.split("}")[-1]: (child.text or "").strip() for child in node}
        title, link = html.unescape(fields.get("title", "")), fields.get("link", "")
        date = parse_date(fields.get("pubDate") or fields.get("date"))
        if title and link.startswith("https://") and date:
            items.append({"title": title, "link": link, "date": date.isoformat(), "source": name})
    return items


def main():
    items = []
    for name, url in FEEDS:
        try:
            items += load(name, url)
        except Exception as e:  # 片方の配信元が落ちていても、もう片方で更新する
            print(f"skip {name}: {e}")

    items = [i for i in items if KEYWORDS.search(i["title"])]
    items.sort(key=lambda i: i["date"], reverse=True)

    seen, result = set(), []
    for item in items:  # 同じ事件を複数の配信元が報じた場合の重複を減らす
        key = re.sub(r"\s", "", item["title"])[:20]
        if key not in seen:
            seen.add(key)
            result.append(item)

    if not result:
        print("no items; keep previous news.json")
        return
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(), "items": result[:MAX_ITEMS]},
                  f, ensure_ascii=False, indent=1)
    print(f"saved {len(result[:MAX_ITEMS])} items")


if __name__ == "__main__":
    main()
