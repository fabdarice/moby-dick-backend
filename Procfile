web: uwsgi --ini=uwsgi.ini --http-socket=127.0.0.1:8080
worker: celery worker --loglevel=info -Q main -A app.celeryconfig -O fair

