import asyncio
from twscrape import API, gather

async def test():
    try:
        api = API()
        print("API created successfully")
        # Simple search for oil-related tweets
        tweets = await gather(api.search("oil -ethanol", limit=5))
        print(f"Found {len(tweets)} tweets")
        for i, tweet in enumerate(tweets[:3]):
            print(f"{i+1}. {tweet.rawContent[:100]}...")
        return tweets
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    asyncio.run(test())