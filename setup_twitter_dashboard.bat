@echo off
cd /d "C:\Users\being\OneDrive\Documents\AI Courses\Personal Website"
title Twitter Dashboard Setup
echo ========================================
echo TWITTER-BASED DASHBOARD SETUP
echo ========================================
echo.
echo This script will set up your Twitter accounts for the daily dashboard update.
echo.
echo Step 1: Editing accounts file...
echo Please edit the accounts.txt file to add your Twitter accounts.
echo Format: username password (one account per line)
echo.
echo Opening accounts.txt in Notepad...
timeout /t 3 /nobreak >nul
notepad.exe "C:\Users\being\OneDrive\Documents\AI Courses\Personal Website\accounts.txt"
echo.
echo Step 2: Logging into Twitter accounts...
echo After you've saved your accounts, this script will log them in.
echo.
pause
echo.
echo Logging into all Twitter accounts...
echo This may take a minute...
twscrape pool login-all
echo.
echo Step 3: Testing the setup...
echo Running a quick test to verify everything works...
python test_twscrape.py
echo.
echo ========================================
echo SETUP COMPLETE
echo ========================================
echo.
echo Your Twitter accounts are now set up for daily dashboard updates.
echo The update_dashboard.bat script will now fetch real-time news from Twitter.
echo.
echo To manually trigger an update, run: update_dashboard.bat
echo.
echo The Windows Task Scheduler will automatically run this daily at 9:09 AM.
echo.
pause