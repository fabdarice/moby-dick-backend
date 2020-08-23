web: uwsgi --ini=uwsgi.ini
worker: celery worker --loglevel=info -Q main -A app.celeryconfig -O fair

