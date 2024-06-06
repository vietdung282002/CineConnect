source /home/site/wwwroot/antenv/bin/activate
cd /home/site/wwwroot
celery -A CineConnect worker --loglevel=info