@echo off
cd /d D:\Ferreteria
set FLASK_APP=app.py
set FLASK_ENV=development

REM Obtén la IP utilizando tu script Python
for /f %%i in ('python obtener_ip.py') do set IP=%%i

start "" http://%IP%:5000
python -m flask run --host=%IP% --port=5000
