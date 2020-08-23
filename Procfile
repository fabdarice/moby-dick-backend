worker: uwsgi --ini=uwsgi.ini --http-socket=0.0.0.0:8080
worker: celery worker --loglevel=info -Q main -A app.celeryconfig -O fair

