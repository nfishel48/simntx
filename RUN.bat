@ECHO OFF
start cmd.exe /K "cd env/Scripts && activate && cd .. && cd .. && echo Virtual environment started && echo. && manage.py runserver"