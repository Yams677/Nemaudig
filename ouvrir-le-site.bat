@echo off
REM Ouvre la maquette C (Anatomie de verre) : relance le serveur local si besoin, puis le navigateur.
cd /d "%~dp0"
powershell -NoProfile -Command "try { Invoke-WebRequest http://127.0.0.1:8785/ -UseBasicParsing -TimeoutSec 2 | Out-Null } catch { Start-Process python -ArgumentList 'serveur.py' -WindowStyle Hidden; Start-Sleep 2 }"
start "" http://localhost:8785/
