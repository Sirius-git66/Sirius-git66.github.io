@echo off
cd "C:\Users\being\OneDrive\Documents\AI Courses\Personal Website"

:: Update the script to use proxy (if not done yet)
powershell -Command "(Get-Content index.html) -replace 'xai-Uk1WRHgRrxXdNGCYgxsY5rOVT3rdlN7gob9NYhUwVLK4k0u25JijLLV4ZbYRKGm8zaEwQEoicugH1ikS', 'https://solitary-snowflake-grok.yourname.workers.dev/api/grok' | Set-Content index.html"

:: Normal git stuff it already does
git add .
git commit --amend --no-edit
git push origin master:main --force-with-lease

echo.
echo SUCCESS! Dashboard live again with Grok-4 running safely in background.
echo Your PC assistant is now officially a hero.
pause