@echo off
echo Updating news section...
powershell -ExecutionPolicy Bypass -File "%~dp0update_news_section.ps1"
echo News section updated!
pause