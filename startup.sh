
# Start Celery worker
celery -A CineConnect worker --loglevel=info -P gevent

# Start Celery Beat
celery -A CineConnect beat --loglevel=info