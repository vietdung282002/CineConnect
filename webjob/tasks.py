from .models import TestWJob
from time import sleep
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

def notify_user():
    # lookup user by id and send them a message
    logger.warning(str(timezone.now()))