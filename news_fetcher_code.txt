#!/usr/bin/env python3
"""
Standalone news fetcher for energy commodities dashboard.
This script can be modified by market analysts to use different RSS sources.
"""

import asyncio
import feedparser
import logging
from datetime import datetime
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataFetcher:
    """Base class for data fetchers"""
    
    async def fetch_url(self, url: str) -> str:
        """Fetch content from URL"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

class NewsFetcher(DataFetcher):
    """Fetch news from RSS feeds"""
    
    async def fetch_news(self, max_items: int = 10) -> List[Dict[str, Any]]:
        """Fetch news from multiple sources"""
        
        # Current RSS sources - modify these based on your preferences
        news_sources = [
            ("Google News - Oil & Gas", "https://news.google.com/rss/search?q=oil+gas+LNG+energy+prices&hl=en-US&gl=US&ceid=US:en"),
            ("Google News - Energy Traders", "https://news.google.com/rss/search?q=Trafigura+OR+Vitol+OR+Gunvor+OR+JERA+OR+Glencore+OR+Shell+Trading&hl=en-US&gl=US&ceid=US:en"),
            ("OilPrice.com", "https://oilprice.com/rss/main"),
        ]
        
        all_news = []
        
        # Keywords to filter for relevant news only
        relevant_keywords = ['oil', 'gas', 'lng', 'power', 'brent', 'wti', 'crude', 'natural gas', 'electricity', 'ttf', 'jkm']
        
        # Target companies to always include
        priority_companies = ['trafigura', 'vitol', 'gunvor', 'jera', 'glencore', 'shell trading', 'total', 'bp trading', 'mercuria', 'cargill']
        
        for source_name, url in news_sources:
            try:
                content = await self.fetch_url(url)
                if content:
                    feed = feedparser.parse(content)
                    
                    for entry in feed.entries[:10]:  # Get more items to filter from
                        title = entry.get('title', 'No title').lower()
                        summary = entry.get('summary', '').lower()
                        
                        # Include if: contains relevant keywords OR mentions priority companies
                        is_relevant = any(keyword in title or keyword in summary for keyword in relevant_keywords)
                        is_company_news = any(company in title or company in summary for company in priority_companies)
                        
                        if is_relevant or is_company_news:
                            # Skip if it's about ethanol, biofuel, renewable diesel, etc.
                            if not any(skip in title or skip in summary for skip in ['ethanol', 'biofuel', 'biodiesel', 'renewable diesel', 'corn']):
                                news_item = {
                                    "title": entry.get('title', 'No title'),
                                    "link": entry.get('link', ''),
                                    "published": entry.get('published', ''),
                                    "source": source_name,
                                    "summary": entry.get('summary', '')[:200] + '...' if entry.get('summary') else ''
                                }
                                all_news.append(news_item)
            except Exception as e:
                logger.error(f"Error fetching news from {source_name}: {str(e)}")
        
        # Sort by published date and return top items
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            except:
                return datetime.min
        
        all_news.sort(key=lambda x: parse_date(x.get('published', '')), reverse=True)
        return all_news[:max_items]

# Example usage
async def main():
    """Example of how to use the NewsFetcher"""
    fetcher = NewsFetcher()
    news_items = await fetcher.fetch_news(max_items=10)
    
    print(f"Found {len(news_items)} news items:")
    for i, item in enumerate(news_items, 1):
        print(f"{i}. {item['title']}")
        print(f"   Source: {item['source']}")
        print(f"   Published: {item['published']}")
        print(f"   Link: {item['link']}")
        print()

if __name__ == "__main__":
    asyncio.run(main())