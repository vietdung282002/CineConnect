from .models import TestWJob
from time import sleep
import logging
from background_task import background
from django.utils import timezone

logger = logging.getLogger(__name__)

@background(schedule=5)
def notify_user():
    # lookup user by id and send them a message
    logger.warning(str(timezone.now()))