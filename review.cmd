@echo off
(
echo ===== GIT STATUS =====
git status

echo ===== GIT LOG =====
git log --oneline -10

echo ===== REMOTES =====
git remote -v

echo ===== PROJECT FILES =====
git ls-files

echo ===== assistant\main.py =====
type assistant\main.py

echo ===== assistant\cdp.py =====
type assistant\cdp.py

echo ===== assistant\jabber.py =====
type assistant\jabber.py

echo ===== assistant\chatgpt.py =====
type assistant\chatgpt.py

echo ===== assistant\bridge.py =====
type assistant\bridge.py
) > review.txt
notepad review.txt
