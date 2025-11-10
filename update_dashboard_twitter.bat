@echo off
echo Updating dashboard with Twitter and RSS news...
echo.

echo 1. Fetching news from Twitter and RSS sources...
python twitter_news_fetcher.py
if %ERRORLEVEL% NEQ 0 (
    echo Error fetching news!
    pause
    exit /b 1
)

echo.
echo 2. Updating dashboard HTML with fresh news...
python update_dashboard_with_twitter_news.py
if %ERRORLEVEL% NEQ 0 (
    echo Error updating dashboard!
    pause
    exit /b 1
)

echo.
echo 3. Updating timestamp...
powershell -Command "(Get-Content 'dashboard.html') -replace 'LAST UPDATE: [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', 'LAST UPDATE: %date:~10,4%-%date:~4,2%-%date:~7,2% %time:~0,2%:%time:~3,2%:00' | Set-Content 'dashboard.html'"

echo.
echo 4. Committing changes to Git...
git add dashboard.html commodities_news.json
git commit -m "Auto-update: Dashboard with fresh Twitter/RSS news"
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Git commit failed!
)

echo.
echo 5. Pushing to GitHub...
git push origin main
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Git push failed!
)

echo.
echo Dashboard updated successfully with Twitter and RSS news!
echo Visit your website to see the latest updates.
echo.
pause