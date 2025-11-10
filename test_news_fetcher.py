#!/usr/bin/env python3
"""
Test script for the standalone news fetcher.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_fetcher_standalone import NewsFetcher

async def test_news_fetcher():
    """Test the NewsFetcher class"""
    print("Testing NewsFetcher...")
    fetcher = NewsFetcher()
    
    try:
        news_items = await fetcher.fetch_news(max_items=5)
        print(f"\nSuccessfully fetched {len(news_items)} news items:\n")
        
        for i, item in enumerate(news_items, 1):
            print(f"{i}. {item['title']}")
            print(f"   Source: {item['source']}")
            print(f"   Published: {item['published']}")
            print(f"   Link: {item['link']}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_news_fetcher())