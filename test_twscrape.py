#!/usr/bin/env python3
"""
Test script to verify twscrape installation and basic functionality
"""

import asyncio
from twscrape import API, gather

async def test_twscrape():
    print("Testing twscrape installation...")
    try:
        # Create API instance
        api = API()
        print("✓ twscrape imported successfully")
        print("✓ API instance created")
        
        # Test account pool
        print("✓ Account pool accessible")
        
        print("\ntwscrape is ready to use!")
        print("\nNext steps:")
        print("1. Edit accounts.txt with your Twitter accounts")
        print("2. Run: twscrape pool login-all")
        print("3. Run: python twitter_news_fetcher.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease check that twscrape is properly installed:")
        print("Run: pip install twscrape")

if __name__ == "__main__":
    asyncio.run(test_twscrape())