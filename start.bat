@echo off

:start
cls

python script.py %*
timeout /t 60 /nobreak
tasklist | find /i "python.exe" >NUL && taskkill /f /im "python.exe" || taskkill /f /im "py.exe"

goto start