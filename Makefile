deps:
	pip install -r requirements.txt

flask:
	pip install -e .
	FLASK_APP=routes.py FLASK_ENV=development flask run

celery:
	celery worker --loglevel=info -Q main -A app.celeryconfig -O fair --beat --pidfile='/tmp/celerybeat.pid'


