# myproject/__init__.py
from __future__ import absolute_import, unicode_literals

# Đảm bảo celery được nạp khi khởi động Django
from .celery import app as celery_app

__all__ = ('celery_app',)