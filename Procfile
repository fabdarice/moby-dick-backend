web: FLASK_APP=routes.py FLASK_ENV=production flask run
worker: celery worker --loglevel=info -Q main -A app.celeryconfig -O fair
