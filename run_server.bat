@echo off
call env\Scripts\activate.bat
set DEBUG=True
set SECRET_KEY=test-secret-key
python manage.py runserver
pause
