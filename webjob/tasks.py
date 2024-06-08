from celery import shared_task
from .models import TestWJob
from time import sleep
import logging

logger = logging.getLogger(__name__)

# @shared_task
# def test():
#     try:
#         logger.info("Task đang chạy mỗi 1 phút")
#         print("Task đang chạy mỗi 1 phút")
#         # Logic của task
#         result = "Task completed"
#         logger.info("Task hoàn thành: %s", result)
#         return result
#     except Exception as e:
#         logger.error("Task gặp lỗi: %s", str(e))
#         raise
    
@shared_task
def my_task():
    try:
        obj = TestWJob.objects.create()
    except:
        print("error")
    return "Task Complete!"