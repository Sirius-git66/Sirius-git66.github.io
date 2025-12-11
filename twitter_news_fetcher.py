#!/usr/bin/env python3
"""
Commodities News Fetcher - RSS Only (No Twitter/X)
Reliable, no blocks, always works
"""

import asyncio
import json
import re
import logging
from datetime import datetime
from pathlib import Path
import aiohttp
import feedparser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_JSON = Path("commodities_news.json")
CACHE_FILE = Path("news_cache.json")
MAX_ITEMS = 15

# RSS SOURCES - Reliable, no paywalls, no blocks
RSS_SOURCES = [
    ("OilPrice.com",   "https://oilprice.com/rss/main"),
    ("EIA",            "https://www.eia.gov/todayinenergy/rss.php"),
    ("LNG World News", "https://www.lngworldnews.com/feed/"),
    ("Rigzone",        "https://www.rigzone.com/news/rss"),
    ("Natural Gas Intel", "https://www.naturalgasintel.com/feed/"),
    ("Energy Voice",   "https://www.energyvoice.com/feed/"),
]

# Keywords for relevance filtering
RELEVANT_KEYWORDS = ['oil', 'gas', 'lng', 'jkm', 'ttf', 'henry hub', 'natural gas', 'power', 
                     'electricity', 'brent', 'wti', 'crude', 'export', 'cargo', 'terminal',
                     'trafigura', 'vitol', 'gunvor', 'jera', 'glencore', 'mercuria', 'opec', 'eia']

# Trash keywords to exclude
TRASH_KEYWORDS = ['crypto', 'bitcoin', 'stock', 'dow', 'nba', 'nfl', 'solar panels', 'ev battery',
                  'ethanol', 'biofuel', 'celebrity', 'entertainment']

def load_cache(): 
    return set(json.loads(CACHE_FILE.read_text())) if CACHE_FILE.exists() else set()

def save_cache(seen): 
    CACHE_FILE.write_text(json.dumps(list(seen)))

def clean_title(title):
    """Remove HTML tags and trim excess text"""
    return re.sub(r'<[^>]+>', '', title).split(' - ')[0].split(' | ')[0].strip()[:200]

async def fetch_rss():
    """Fetch news from RSS sources only"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    items = []
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as s:
        for name, url in RSS_SOURCES:
            try:
                async with s.get(url) as r:
                    if r.status != 200: 
                        logger.warning(f"{name}: HTTP {r.status}")
                        continue
                    feed = feedparser.parse(await r.text())
                    for e in feed.entries[:15]:
                        title = clean_title(e.get('title', 'No title'))
                        title_lower = title.lower()
                        
                        # Filter: must contain relevant keywords, exclude trash
                        if not any(kw in title_lower for kw in RELEVANT_KEYWORDS):
                            continue
                        if any(trash in title_lower for trash in TRASH_KEYWORDS):
                            continue
                        
                        link = e.link.split('?')[0] if isinstance(e.link, str) else str(e.link)
                        summary_raw = e.get('summary', '') or ''
                        if not isinstance(summary_raw, str):
                            summary_raw = str(summary_raw)
                        summary = re.sub('<.*?>', '', summary_raw)[:250]
                        
                        items.append({
                            "title": title,
                            "link": link,
                            "summary": summary,
                            "source": name,
                            "published": "Recent",
                            "sort_date": datetime.now()
                        })
                        
                        if len(items) >= 30:  # Collect enough items for filtering
                            break
            except Exception as e:
                logger.warning(f"Error fetching {name}: {e}")
    return items

async def main():
    seen = load_cache()
    all_items = []

    # Fetch from RSS sources
    logger.info("Fetching commodities news from RSS sources...")
    rss_items = await fetch_rss()
    all_items.extend(rss_items)
    logger.info(f"RSS gave {len(rss_items)} items")

    # Dedupe & sort by date
    for item in all_items:
        if item['sort_date'].tzinfo is not None:
            item['sort_date'] = item['sort_date'].replace(tzinfo=None)
    
    all_items.sort(key=lambda x: x['sort_date'], reverse=True)
    fresh = []
    new_links = set()
    for item in all_items:
        if item['link'] not in seen and len(fresh) < MAX_ITEMS:
            fresh.append(item)
            new_links.add(item['link'])

    # Update cache with new links
    seen.update(new_links)
    save_cache(seen)

    # Save JSON for website
    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "items": [{k:v for k,v in item.items() if k != "sort_date"} for item in fresh]
    }
    OUTPUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    logger.info(f"✓ Saved {len(fresh)} fresh headlines to {OUTPUT_JSON}")
    
    # Print preview
    print(f"\n{'='*60}")
    print(f"COMMODITIES NEWS UPDATE - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    for i, it in enumerate(fresh[:10], 1):
        print(f"{i}. {it['title']}")
        print(f"   {it['source']} | {it['link']}\n")
    print(f"{'='*60}")
    print(f"Total: {len(fresh)} headlines | No Twitter errors!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(main())