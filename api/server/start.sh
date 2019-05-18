cd /code/server
gunicorn -w 4 -b 0.0.0.0:3000 application
