web: gunicorn CineConnect.wsgi
worker: celery -A CineConnect worker --loglevel=info --pool=eventlet