@echo off
echo Syncing JobNimbus Data...
"backend\venv\Scripts\python.exe" backend/sync_service.py
echo Sync Complete.
pause
