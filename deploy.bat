@echo off
REM Deployment script for GitHub Pages

REM Create deployment directory
mkdir ..\deployment

REM Copy static files
copy *.html ..\deployment\
if exist *.css copy *.css ..\deployment\
if exist *.js copy *.js ..\deployment\
if exist images\ xcopy images\ ..\deployment\images\ /E /I
if exist *.jpg copy *.jpg ..\deployment\
if exist *.png copy *.png ..\deployment\

REM Remove proxy server files (not needed for static hosting)
del ..\deployment\grok_proxy.py 2>nul
del ..\deployment\requirements.txt 2>nul
del ..\deployment\start_servers.bat 2>nul
del ..\deployment\test_grok.html 2>nul
del ..\deployment\deploy.bat 2>nul
del ..\deployment\deploy.sh 2>nul

echo Deployment package created in ..\deployment\
echo To deploy to GitHub Pages:
echo 1. Create a new repository on GitHub
echo 2. Copy the files from ..\deployment\ to your repository
echo 3. Enable GitHub Pages in your repository settings