@echo off
echo Starting GROK proxy server and main website server...

REM Start the GROK proxy server in the background
start "GROK Proxy Server" cmd /k "python grok_proxy.py"

REM Wait a moment for the proxy to start
timeout /t 3 /nobreak >nul

REM Start the main website server
python -m http.server 8000