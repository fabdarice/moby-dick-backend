web: uwsgi --ini=uwsgi.ini --http :$PORT
worker: celery worker --loglevel=info -Q main -A app.celeryconfig -O fair

