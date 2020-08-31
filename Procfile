web: uwsgi --ini=uwsgi.ini --http :$PORT
worker: celery worker -c 2 --loglevel=info -Q main -A app.celeryconfig -O fair --beat --pidfile="/tmp/celerybeat.pid"

