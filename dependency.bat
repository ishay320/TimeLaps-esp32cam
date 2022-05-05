set env=timelapsESP32_env
python -m venv %env%
.\%env%\scripts\python.exe -m pip install --upgrade pip
.\%env%\scripts\python.exe -m pip install -r "requirements.txt"
