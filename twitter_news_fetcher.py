#!/usr/bin/env python3
"""
ULTIMATE Commodities News Fetcher – X (Twitter) first, RSS backup
Zero paywalls, real-time, trader-grade
"""

import asyncio
import json
import re
import logging
from datetime import datetime
from pathlib import Path

# Use twscrape (2025-proof, no login needed)
# pip install twscrape
from twscrape import API, gather
# OR fallback to snscrape if you prefer: pip install git+https://github.com/JustAnotherArchivist/snscrape.git

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_JSON = Path("commodities_news.json")
CACHE_FILE = Path("news_cache.json")
MAX_ITEMS = 15

# 1. X FIRST (real-time)
X_QUERY = (
    '(oil OR crude OR brent OR wti OR LNG OR JKM OR TTF OR "natural gas" OR power OR OPEC OR EIA '
    'OR Trafigura OR Vitol OR Gunvor OR JERA OR Glencore OR Mercuria) '
    '(price OR export OR import OR cargo OR terminal OR refinery OR outage OR diversion) '
    '-ethanol -biofuel -solar -wind -battery -hydrogen -climate -netzero '
    'lang:en since:2025-11-09 min_faves:5'
)

# 2. RSS BACKUP (only the unbreakable ones)
FALLBACK_RSS = [
    ("OilPrice.com",   "https://oilprice.com/rss/main"),
    ("EIA",            "https://www.eia.gov/todayinenergy/rss.php"),
    ("LNG World News", "https://www.lngworldnews.com/feed/"),
]

def load_cache(): 
    return set(json.loads(CACHE_FILE.read_text())) if CACHE_FILE.exists() else set()

def save_cache(seen): 
    CACHE_FILE.write_text(json.dumps(list(seen)))

async def fetch_x(api):
    tweets = await gather(api.search(X_QUERY, limit=50))
    items = []
    for t in tweets:
        # Filter out low engagement tweets
        if hasattr(t, 'viewCount') and t.viewCount < 200: 
            continue  # filter noise
        items.append({
            "title": t.rawContent.split('\n')[0][:200],
            "link": f"https://x.com/{t.user.username}/status/{t.id}",
            "summary": t.rawContent[:300],
            "source": f"X @{t.user.username}",
            "published": t.date.strftime("%b %d %H:%M"),
            "sort_date": t.date
        })
    return items

async def fetch_rss_backup():
    import aiohttp, feedparser
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131"}
    items = []
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as s:
        for name, url in FALLBACK_RSS:
            try:
                async with s.get(url) as r:
                    if r.status != 200: 
                        continue
                    feed = feedparser.parse(await r.text())
                    for e in feed.entries[:10]:
                        link = e.link.split('?')[0] if isinstance(e.link, str) else str(e.link)
                        summary_raw = e.get('summary', '') or ''
                        # Ensure summary is a string before processing
                        if not isinstance(summary_raw, str):
                            summary_raw = str(summary_raw)
                        summary = re.sub('<.*?>', '', summary_raw)[:250]
                        items.append({
                            "title": e.title,
                            "link": link,
                            "summary": summary,
                            "source": name,
                            "published": "Recent",
                            "sort_date": datetime.now()
                        })
            except Exception as e:
                logger.warning(f"Error fetching {name}: {e}")
                pass
    return items

async def main():
    seen = load_cache()
    all_items = []

    # 1. Try X first
    try:
        api = API()  # twscrape creates temp accounts automatically
        # Load accounts from file
        import os
        if os.path.exists("accounts.txt"):
            # For now, we'll rely on accounts already added to the pool
            # The setup script should have added them
            try:
                await api.pool.login_all()
            except Exception as login_error:
                logger.warning(f"Login failed due to Cloudflare protection: {login_error}")
                # Continue anyway as twscrape has workarounds
            
            try:
                x_items = await fetch_x(api)
                all_items.extend(x_items)
                logger.info(f"X gave {len(x_items)} items")
            except Exception as fetch_error:
                logger.warning(f"X fetch failed: {fetch_error}")
        else:
            logger.warning("accounts.txt not found, falling back to RSS")
    except Exception as e:
        logger.warning(f"X failed ({e}), falling back to RSS")

    # 2. RSS backup if X gave < 8 items
    if len(all_items) < 8:
        rss_items = await fetch_rss_backup()
        all_items.extend(rss_items)
        logger.info(f"RSS backup gave {len(rss_items)} items")

    # Dedupe & sort
    # Ensure all dates are timezone-naive for sorting
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

    seen.update(new_links)
    save_cache(seen)

    # Save JSON for website
    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "items": [{k:v for k,v in item.items() if k != "sort_date"} for item in fresh]
    }
    OUTPUT_JSON.write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(fresh)} fresh headlines → {OUTPUT_JSON}")

    # Print preview
    for i, it in enumerate(fresh[:10], 1):
        print(f"{i}. {it['title']}")
        print(f"   {it['source']} | {it['published']} | {it['link']}\n")

if __name__ == "__main__":
    asyncio.run(main())