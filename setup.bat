@echo off
title NEXUS Setup
color 0a

echo =============================================
echo         NEXUS - Pentest Framework Setup
echo         Authorized Use Only
echo =============================================
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Run as Administrator!
    pause
    exit /b 1
)

echo [*] Checking Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Python missing. Install Python 3.11+ first.
    pause
    exit /b 1
)

echo [*] Installing dependencies...
pip install -r requirements.txt
echo [+] Dependencies installed.

echo [*] Checking Tor...
where tor >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Tor not found. Install Tor Browser from torproject.org
)

echo [*] Hiding project folder...
attrib +h "%CD%" /s /d >nul 2>&1

echo.
echo =============================================
echo      SETUP COMPLETE
echo      Run: python main.py
echo =============================================
pause