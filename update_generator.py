import re

# Read the file
with open(r"C:\Users\being\OneDrive\Documents\Projects\Web Scrape\commodities_dashboard.py", 'r', encoding='utf-8') as f:
    content = f.read()

# First replacement: Add CSS for guide section (already done via PowerShell, so skip)

# Second replacement: Update HTML to wrap news in grid and add guide section
old_html = r'''        
        <!-- News Section -->
        <div class="news-section">
            <div class="card-title">Market News</div>
            {render_news(news_data)}
        </div>
    </div>
</body>
</html>"""'''

new_html = r'''        
        <!-- News and Guide Grid -->
        <div class="bottom-grid">
            <!-- News Section -->
            <div class="news-section">
                <div class="card-title">Market News</div>
                {render_news(news_data)}
            </div>
            
            <!-- Educational Guide Section -->
            <div class="guide-section">
                <a href="commodity-trading-guide.html" target="_blank" class="guide-link">
                    <div class="guide-text">Free Educational Guide</div>
                    <div class="guide-icon-container">
                        <img src="Guide_Logo.png" alt="Educational Guide" class="guide-icon">
                    </div>
                </a>
            </div>
        </div>
    </div>
</body>
</html>"""'''

content = content.replace(old_html, new_html)

# Write back
with open(r"C:\Users\being\OneDrive\Documents\Projects\Web Scrape\commodities_dashboard.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ commodities_dashboard.py updated successfully!")
