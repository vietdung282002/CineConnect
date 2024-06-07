export LANG=C.UTF-8

gunicorn — bind=0.0.0.0 — timeout 600 CineConnect.wsgi & celery -A CineConnect worker -l INFO -B