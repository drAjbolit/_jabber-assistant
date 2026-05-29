@echo off
(
echo ===== GIT STATUS =====
git status
echo.
echo ===== GIT LOG =====
git log --oneline -10
echo.
echo ===== REMOTES =====
git remote -v
echo.
echo ===== PROJECT FILES =====
git ls-files
echo.
echo ===== assistant\main.py =====
type assistant\main.py
echo.
echo ===== assistant\cdp.py =====
type assistant\cdp.py
echo.
echo ===== assistant\jabber.py =====
type assistant\jabber.py
echo.
echo ===== assistant\chatgpt.py =====
type assistant\chatgpt.py
echo.
echo ===== assistant\bridge.py =====
type assistant\bridge.py
) > review.txt
notepad review.txt
