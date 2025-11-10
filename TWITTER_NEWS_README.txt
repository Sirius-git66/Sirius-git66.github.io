TWITTER-BASED COMMODITIES NEWS FETCHER
=====================================

This system fetches real-time commodities news from Twitter (X) and falls back to RSS sources when needed.

SETUP INSTRUCTIONS:
------------------

1. Edit accounts.txt to add 4-5 throwaway Twitter accounts:
   - Format: username password (one account per line)
   - Example:
     user1 pass1
     user2 pass2
     user3 pass3

2. Login to all accounts:
   - Run: twscrape pool login-all

3. Test the system:
   - Run: fetch_twitter_news.bat
   - Or run: python twitter_news_fetcher.py

USAGE:
-----

Option 1: Run the complete workflow (fetch news + update dashboard + push to GitHub):
  - Run: update_dashboard_twitter.bat

Option 2: Run individual components:
  - Fetch news: fetch_twitter_news.bat
  - Update dashboard: python update_dashboard_with_twitter_news.py

HOW IT WORKS:
------------

1. Twitter First Approach:
   - Searches Twitter for real-time commodities news
   - Filters for high-engagement tweets (200+ views)
   - Focuses on oil, gas, LNG, power, and major trading companies

2. RSS Backup:
   - If Twitter doesn't provide enough news, falls back to RSS sources
   - Uses OilPrice.com, EIA, and LNG World News

3. Dashboard Update:
   - Replaces the Market News section with fresh content
   - Updates the timestamp
   - Pushes changes to your GitHub website

BENEFITS:
--------

- Real-time news from Twitter (trader-grade)
- No paywalls or subscriptions required
- Automatic fallback to RSS when Twitter is unavailable
- Maintains your existing dashboard layout
- Fully automated workflow

TROUBLESHOOTING:
---------------

If you get authentication errors:
- Verify accounts.txt contains valid Twitter accounts
- Run: twscrape pool login-all

If you get "No module named twscrape":
- Run: pip install twscrape

If Twitter fetching fails:
- The system will automatically fall back to RSS sources