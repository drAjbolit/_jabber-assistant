@echo off

echo Creating run.cmd...
(
echo @echo off
echo call .venv\Scripts\activate.bat
echo python -m assistant.main
) > run.cmd

echo Creating git_push.cmd...
(
echo @echo off
echo call .venv\Scripts\activate.bat
echo git add .
echo git commit -m "auto update"
echo git push
echo pause
) > git_push.cmd

echo Creating review.cmd...
(
echo @echo off
echo ^(
echo echo ===== GIT STATUS =====
echo git status
echo.
echo echo ===== GIT LOG =====
echo git log --oneline -10
echo.
echo echo ===== REMOTES =====
echo git remote -v
echo.
echo echo ===== PROJECT FILES =====
echo git ls-files
echo.
echo echo ===== assistant\main.py =====
echo type assistant\main.py
echo.
echo echo ===== assistant\cdp.py =====
echo type assistant\cdp.py
echo.
echo echo ===== assistant\jabber.py =====
echo type assistant\jabber.py
echo.
echo echo ===== assistant\chatgpt.py =====
echo type assistant\chatgpt.py
echo.
echo echo ===== assistant\bridge.py =====
echo type assistant\bridge.py
echo ^) ^> review.txt
echo notepad review.txt
) > review.cmd

echo.
echo DONE
echo.
dir *.cmd

pause