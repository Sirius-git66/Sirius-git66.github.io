#!/bin/bash
# Deployment script for GitHub Pages

# Create deployment directory
mkdir -p ../deployment

# Copy static files
cp *.html ../deployment/
cp -r *.css ../deployment/ 2>/dev/null || true
cp -r *.js ../deployment/ 2>/dev/null || true
cp -r images/ ../deployment/ 2>/dev/null || true
cp -r *.jpg ../deployment/ 2>/dev/null || true
cp -r *.png ../deployment/ 2>/dev/null || true

# Remove proxy server files (not needed for static hosting)
rm -f ../deployment/grok_proxy.py
rm -f ../deployment/requirements.txt
rm -f ../deployment/start_servers.bat
rm -f ../deployment/test_grok.html
rm -f ../deployment/deploy.sh

echo "Deployment package created in ../deployment/"
echo "To deploy to GitHub Pages:"
echo "1. Create a new repository on GitHub"
echo "2. Copy the files from ../deployment/ to your repository"
echo "3. Enable GitHub Pages in your repository settings"