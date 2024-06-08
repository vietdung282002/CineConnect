celery -A CineConnect worker --loglevel=info &
celery -A CineConnect beat --loglevel=info &