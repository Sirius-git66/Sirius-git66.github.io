#!/usr/bin/env python3
"""
Energy Commodities News Fetcher – 100% FREE, NO PAYWALLS
Tested working Nov 10 2025
"""

import asyncio
import feedparser
import logging
import json
import re
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OUTPUT_JSON = Path("commodities_news.json")
CACHE_FILE = Path("news_cache.json")
MAX_ITEMS = 15

# 100% FREE & SCRIPT-FRIENDLY SOURCES (NO paid subscriptions)
NEWS_SOURCES = [
    ("EIA Today in Energy",          "https://www.eia.gov/todayinenergy/rss.php"),
    ("OPEC Press Room",              "https://www.opec.org/opec_web/en/rss/press_room.xml"),
    ("LNG World News",               "https://www.lngworldnews.com/feed/"),
    ("Offshore Energy",              "https://www.offshore-energy.biz/feed/"),
    ("OilPrice.com",                 "https://oilprice.com/rss/main"),
    ("Energy Voice",                 "https://www.energyvoice.com/feed/"),
    ("Google News Oil&LNG",          "https://news.google.com/rss/search?q=(oil+OR+crude+OR+brent+OR+wti+OR+LNG+OR+JKM+OR+TTF+OR+Henry+Hub)+when:1d&hl=en-US&gl=US&ceid=US:en"),
]

RELEVANT_KEYWORDS = ['oil','crude','brent','wti','lng','jkm','ttf','henry hub','natural gas','power','electricity','opec','eia']
PRIORITY_COMPANIES = ['trafigura','vitol','gunvor','jera','glencore','shell','totalenergies','bp','mercuria']
SKIP_PHRASES = ['ethanol','biofuel','solar','wind','battery','hydrogen','carbon capture','climate','net zero','ev ','electric vehicle']

def load_cache(): 
    return set(json.loads(CACHE_FILE.read_text())) if CACHE_FILE.exists() else set()

def save_cache(seen): 
    CACHE_FILE.write_text(json.dumps(list(seen)))

def is_relevant(text):
    text = text.lower()
    return ((any(k in text for k in RELEVANT_KEYWORDS) or any(c in text for c in PRIORITY_COMPANIES))
            and not any(s in text for s in SKIP_PHRASES))

def smart_date(entry):
    date_str = entry.get('published') or entry.get('updated') or ''
    for fmt in ('%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S'):
        try: 
            dt = datetime.strptime(date_str.strip(), fmt)
            # Convert to naive datetime if timezone aware
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        except: pass
    return datetime.min

class NewsFetcher:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131 Safari/537.36"}

    async def fetch(self, url):
        import aiohttp
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(headers=self.headers) as s:
            async with s.get(url, timeout=timeout) as r:
                return await r.text() if r.status == 200 else ""

    async def process(self, name, url, seen):
        content = await self.fetch(url)
        if not content: return []
        feed = feedparser.parse(content)
        items = []
        for e in feed.entries[:25]:
            title = e.get('title', '')
            summary_raw = e.get('summary', '') or ''
            # Ensure summary is a string before processing
            if not isinstance(summary_raw, str):
                summary_raw = str(summary_raw)
            summary = re.sub('<[^>]+>', '', summary_raw)
            text = f"{title} {summary}".lower()
            link_raw = e.get('link', '')
            # Ensure link is a string before splitting
            if not isinstance(link_raw, str):
                link = str(link_raw)
            else:
                link = link_raw.split('?')[0] if link_raw else ''
            if not is_relevant(text): continue
            date = smart_date(e)
            items.append({
                "title": title,
                "link": link,
                "summary": summary[:230] + "..." if len(summary)>230 else summary,
                "source": name,
                "published": date.strftime("%b %d %H:%M") if date != datetime.min else "Recent",
                "date_sort": date
            })
        logger.info(f"{name}: {len(items)} relevant")
        return items

    async def run(self):
        seen = load_cache()
        tasks = [self.process(name, url, seen) for name, url in NEWS_SOURCES]
        results = await asyncio.gather(*tasks)
        all_news = [item for sublist in results for item in sublist]
        all_news.sort(key=lambda x: x['date_sort'], reverse=True)

        fresh = []
        new_links = set()
        for item in all_news:
            if item['link'] not in seen and len(fresh) < MAX_ITEMS:
                fresh.append(item)
                new_links.add(item['link'])

        seen.update(new_links)
        save_cache(seen)

        output = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "items": [{k: v for k, v in item.items() if k != "date_sort"} for item in fresh]
        }
        OUTPUT_JSON.write_text(json.dumps(output, indent=2))
        logger.info(f"Saved {len(fresh)} new headlines → {OUTPUT_JSON}")

        for i, it in enumerate(fresh, 1):
            print(f"{i}. {it['title']}")
            print(f"   {it['source']} | {it['published']} | {it['link']}\n")

if __name__ == "__main__":
    asyncio.run(NewsFetcher().run())