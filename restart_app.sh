pkill gunicorn
venv/bin/gunicorn manage:app --bind 127.0.0.1:5000 -D
