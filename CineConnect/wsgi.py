"""
WSGI config for CineConnect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
settings_module = 'CineConnect.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'CineConnect.settings'
print("test1233212421212")
for test in os.environ:
    print(test)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
