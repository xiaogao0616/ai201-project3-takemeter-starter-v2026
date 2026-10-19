"""Pull recent r/MCFC posts from the RSS feed into raw_posts.csv.

Reddit blocks the .json endpoint for scripts, but the Atom feed still works.
Columns: text (title + body), link (where the post points), id.
"""
import csv, html, re, time
import xml.etree.ElementTree as ET
import requests

HEADERS = {"User-Agent": "takemeter-class-project/0.1"}
NS = {"a": "http://www.w3.org/2005/Atom"}
TARGET = 400


def body_text(content_html):
    # The self-text sits between SC_OFF/SC_ON markers; link/image posts have none.
    m = re.search(r"<!-- SC_OFF -->(.*?)<!-- SC_ON -->", content_html, re.S)
    if not m:
        return ""
    text = re.sub(r"<br\s*/?>|</p>|</li>", "\n", m.group(1))
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\n{2,}", "\n", text).strip()


def link_target(content_html):
    m = re.search(r'<a href="([^"]+)">\[link\]</a>', content_html)
    return html.unescape(m.group(1)) if m else ""


rows, seen, after = [], set(), None
while len(rows) < TARGET:
    url = "https://www.reddit.com/r/MCFC/new/.rss?limit=100" + (f"&after={after}" if after else "")
    for wait in (0, 15, 30, 60, 120):  # back off when Reddit rate-limits (429)
        time.sleep(wait)
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 429:
            break
    r.raise_for_status()
    entries = ET.fromstring(r.content).findall("a:entry", NS)
    if not entries:
        break
    for e in entries:
        pid = e.find("a:id", NS).text
        if pid in seen:
            continue
        seen.add(pid)
        content = e.find("a:content", NS).text or ""
        title = e.find("a:title", NS).text or ""
        body = body_text(content)
        rows.append({"text": (title + "\n" + body).strip(), "link": link_target(content), "id": pid})
    after = entries[-1].find("a:id", NS).text
    time.sleep(2)

with open("raw_posts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["text", "link", "id"])
    w.writeheader()
    w.writerows(rows)
print(len(rows), "posts saved to raw_posts.csv")
