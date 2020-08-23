deps:
	pip install -r requirements.txt

redis:
	redis-server /usr/local/etc/redis.conf --daemonize yes

flask:
	pip install -e .
	FLASK_APP=routes.py FLASK_ENV=development flask run

celery: redis
	celery worker --loglevel=info -Q main -A app.celeryconfig -O fair

