@echo off
echo Generating Commodities Dashboard...
python "C:\Users\being\OneDrive\Documents\Projects\Web Scrape\commodities_dashboard.py"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Dashboard generated successfully!
    
    echo Copying dashboard to website folder...
    copy "C:\Users\being\OneDrive\Documents\Projects\Web Scrape\output\dashboard.html" "C:\Users\being\OneDrive\Documents\AI Courses\Personal Website\dashboard.html"
    
    echo Updating news section with Twitter and RSS articles...
    cd "C:\Users\being\OneDrive\Documents\AI Courses\Personal Website"
    python twitter_news_fetcher.py
    if %ERRORLEVEL% NEQ 0 (
        echo Warning: Twitter news fetch failed, continuing with dashboard update...
    )
    python update_dashboard_with_twitter_news.py
    
    echo Updating website on GitHub...
    git add dashboard.html
    git commit -m "Auto-update: Commodities dashboard refreshed"
    git push origin master:main
    
    echo.
    echo Website updated successfully! Visit https://thearc.cloud/dashboard.html
    echo Opening dashboard in browser...
    start "C:\Users\being\OneDrive\Documents\Projects\Web Scrape\output\dashboard.html"
) else (
    echo.
    echo Error generating dashboard.
    pause
)