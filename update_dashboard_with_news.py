#!/usr/bin/env python3
"""
Update the dashboard HTML with fresh news from the JSON file.
This script integrates the improved news fetcher with your existing dashboard.
"""

import json
from pathlib import Path
from datetime import datetime

def update_dashboard_news():
    """Update the dashboard HTML with fresh news"""
    
    # Paths
    json_file = Path("commodities_news.json")
    dashboard_file = Path("dashboard.html")
    
    # Check if files exist
    if not json_file.exists():
        print("News JSON file not found. Run the news fetcher first.")
        return False
        
    if not dashboard_file.exists():
        print("Dashboard HTML file not found.")
        return False
    
    # Load the fresh news
    try:
        # Try UTF-8 first, then fallback to latin-1
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                news_data = json.load(f)
        except UnicodeDecodeError:
            with open(json_file, 'r', encoding='latin-1') as f:
                news_data = json.load(f)
    except Exception as e:
        print(f"Error loading news JSON: {e}")
        return False
    
    # Read the dashboard HTML
    try:
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            dashboard_content = f.read()
    except Exception as e:
        print(f"Error reading dashboard HTML: {e}")
        return False
    
    # Find the news section in the HTML
    # Look for the market news section
    import re
    # Pattern to match the news section
    pattern = r'(<div class="news-section">.*?class="card-title">Market News</div>).*?(</div>\s*</div>\s*</div>)'
    
    match = re.search(pattern, dashboard_content, re.DOTALL)
    if not match:
        print("Could not find news section in dashboard HTML")
        return False
    
    # Extract parts of the HTML
    before_news = dashboard_content[:match.start(1)]
    after_news = dashboard_content[match.end(2):]
    
    # Generate new news items HTML
    news_items_html = ""
    for item in news_data.get("items", []):
        news_items_html += f'''
                <div class="news-item">
                    <a href="{item["link"]}" target="_blank" class="news-title">{item["title"]}</a>
                    <div class="news-meta">
                        <span class="news-source">{item["source"]}</span>
                        <span class="news-date">{item["published"]}</span>
                    </div>
                </div>
                '''
    
    # Create the new news section
    new_news_section = f'''<div class="news-section">
            <div class="card-title">Market News</div>
{news_items_html}
        </div>'''
    
    # Combine everything
    new_dashboard_content = before_news + new_news_section + after_news
    
    # Write back to file
    try:
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(new_dashboard_content)
        print(f"Dashboard updated with {len(news_data.get('items', []))} fresh news items!")
        print(f"Last updated: {news_data.get('last_updated', 'Unknown')}")
        return True
    except Exception as e:
        print(f"Error writing updated dashboard: {e}")
        return False

if __name__ == "__main__":
    update_dashboard_news()