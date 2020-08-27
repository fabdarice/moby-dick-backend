web: uwsgi --ini=uwsgi.ini --http :$PORT
worker: celery worker --loglevel=info -Q main -A app.celeryconfig -O fair
beat: celery -A app.celeryconfig beat --pidfile="/tmp/celerybeat.pid"

