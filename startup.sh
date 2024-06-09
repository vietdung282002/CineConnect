gunicorn --bind=0.0.0.0 --timeout 600 --workers=4 --chdir CineConnect.wsgi --access-logfile '-' --error-logfile '-'
# Start Celery worker
celery -A CineConnect worker --loglevel=info -P gevent

# Start Celery Beat
celery -A CineConnect beat --loglevel=info