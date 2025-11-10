#!/usr/bin/env python3
"""
Enhanced Energy Commodities News Fetcher (Oil, LNG, Power)
Free sources only — no Bloomberg/Reuters needed.
Run every 15–60 min via cron.
"""

import asyncio
import feedparser
import logging
import json
import re
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

# ----------------------------- CONFIG -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Output file (for your website)
OUTPUT_JSON = Path("commodities_news.json")
CACHE_FILE = Path("news_cache.json")  # remembers seen items

# How many items to return
MAX_ITEMS = 15

# --------------------------- SOURCES ---------------------------
NEWS_SOURCES = [
    # High-quality free RSS feeds (updated 2025)
    ("EIA Today in Energy", "https://www.eia.gov/todayinenergy/rss.php"),
    ("OPEC Press Room", "https://www.opec.org/opec_web/en/rss/press_room.xml"),
    ("S&P Global Commodity Insights", "https://www.spglobal.com/commodityinsights/en/rss"),
    ("ICIS Energy", "https://www.icis.com/explore/rss/commodities/energy/"),
    ("Argus Media Latest", "https://www.argusmedia.com/en/rss/latest-news"),
    ("LNG World News", "https://www.lngworldnews.com/feed/"),
    ("Natural Gas Intelligence", "https://www.naturalgasintel.com/feed/"),
    ("Power Magazine", "https://www.powermag.com/feed/"),
    ("OilPrice.com", "https://oilprice.com/rss/main"),
    ("Rigzone News", "https://www.rigzone.com/news/rss"),
    # Google News fallback (still works sometimes with good headers)
    ("Google News Oil&LNG", "https://news.google.com/rss/search?q=(oil+OR+crude+OR+brent+OR+wti+OR+LNG+OR+JKM+OR+TTF+OR+Henry+Hub)+when:1d&hl=en-US&gl=US&ceid=US:en"),
]

# -------------------------- FILTERS --------------------------
RELEVANT_KEYWORDS = [
    'oil', 'crude', 'brent', 'wti', 'lng', 'natural gas', 'jkm', 'ttf',
    'henry hub', 'power', 'electricity', 'gas-fired', 'coal', 'naphtha',
    'propane', 'butane', 'shale', 'opec', 'eia', 'iea'
]

PRIORITY_COMPANIES = [
    'trafigura', 'vitol', 'gunvor', 'jera', 'glencore', 'shell trading',
    'totalenergies', 'bp trading', 'mercuria', 'cargill', 'koch', 'hartree'
]

SKIP_PHRASES = [
    'ethanol', 'biofuel', 'biodiesel', 'renewable diesel', 'corn', 'solar',
    'wind', 'battery', 'ev ', 'electric vehicle', 'hydrogen', 'carbon capture',
    'climate', 'net zero', 'paris agreement', 'cop', 'football', 'nfl'
]

# -------------------------- HELPERS --------------------------
def load_cache() -> set:
    if CACHE_FILE.exists():
        try:
            return set(json.loads(CACHE_FILE.read_text()))
        except:
            return set()
    return set()

def save_cache(seen: set):
    CACHE_FILE.write_text(json.dumps(list(seen)))

def clean_text(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).lower()  # strip HTML

def is_relevant(title: str, summary: str) -> bool:
    text = f"{title} {summary}".lower()
    has_keyword = any(k in text for k in RELEVANT_KEYWORDS)
    has_company = any(c in text for c in PRIORITY_COMPANIES)
    has_skip = any(s in text for s in SKIP_PHRASES)
    return (has_keyword or has_company) and not has_skip

def smart_parse_date(entry) -> datetime:
    for key in ('published', 'updated', 'pubDate', 'dc:date', 'date'):
        date_str = entry.get(key)
        if not date_str:
            continue
        # Try common formats
        for fmt in (
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S %Z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
        ):
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                # Convert to naive datetime if timezone aware
                if dt.tzinfo is not None:
                    dt = dt.replace(tzinfo=None)
                return dt
            except:
                continue
    return datetime.min

# ---------------------------- FETCHER ------------------------
class NewsFetcher:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, text/xml;q=0.9, */*;q=0.8"
    }

    async def fetch_url(self, url: str) -> str:
        import aiohttp
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(headers=self.headers, timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.warning(f"HTTP {resp.status} for {url}")
                    return ""
                return await resp.text()

    async def fetch_all(self) -> List[Dict[str, Any]]:
        seen_links = load_cache()
        all_news = []
        tasks = []

        for name, url in NEWS_SOURCES:
            tasks.append(self.process_source(name, url, seen_links))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception) or not isinstance(result, list):
                continue
            all_news.extend(result)

        # Sort by date
        all_news.sort(key=lambda x: x['published_parsed'], reverse=True)
        unique_news = []
        new_links = set()

        for item in all_news:
            link = item['link']
            if link not in seen_links:
                unique_news.append(item)
                new_links.add(link)
                if len(unique_news) >= MAX_ITEMS * 2:  # buffer
                    break

        # Update cache
        seen_links.update(new_links)
        save_cache(seen_links)

        return unique_news[:MAX_ITEMS]

    async def process_source(self, name: str, url: str, seen_links: set) -> List[Dict]:
        try:
            content = await self.fetch_url(url)
            if not content:
                return []

            feed = feedparser.parse(content)
            if not feed.entries:
                logger.info(f"No entries from {name}")
                return []

            items = []
            for entry in feed.entries[:20]:  # more to filter from
                title = entry.get('title', 'No title')
                summary_raw = entry.get('summary', '') or entry.get('description', '')
                # Ensure summary is a string before cleaning
                if not isinstance(summary_raw, str):
                    summary_raw = str(summary_raw)
                summary = clean_text(summary_raw)
                link_raw = entry.get('link', '')
                # Ensure link is a string before splitting
                if not isinstance(link_raw, str):
                    link = str(link_raw)
                else:
                    link = link_raw.split('?')[0] if link_raw else ''  # clean tracking params

                # Ensure title is a string before converting to lowercase
                if not isinstance(title, str):
                    title = str(title)
                
                if not is_relevant(title.lower(), summary):
                    continue

                published = smart_parse_date(entry)
                items.append({
                    "title": title,
                    "link": link,
                    "summary": summary[:250] + ("..." if len(summary) > 250 else ""),
                    "source": name,
                    "published": published.strftime("%Y-%m-%d %H:%M") if published != datetime.min else "Recent",
                    "published_parsed": published
                })
            logger.info(f"{name}: {len(items)} relevant items")
            return items

        except Exception as e:
            logger.error(f"Error fetching {name}: {e}")
            return []

# ------------------------------ MAIN ------------------------------
async def main():
    fetcher = NewsFetcher()
    news = await fetcher.fetch_all()

    # Save for website
    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": [
            {
                "title": item["title"],
                "link": item["link"],
                "summary": item["summary"],
                "source": item["source"],
                "published": item["published"]
            }
            for item in news
        ]
    }

    OUTPUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    logger.info(f"Saved {len(news)} fresh headlines to {OUTPUT_JSON}")

    # Pretty print to console
    print(f"\n=== LATEST {len(news)} COMMODITIES HEADLINES ===\n")
    for i, item in enumerate(news, 1):
        print(f"{i}. {item['title']}")
        print(f"   {item['source']} | {item['published']}")
        print(f"   {item['link']}\n")

if __name__ == "__main__":
    asyncio.run(main())