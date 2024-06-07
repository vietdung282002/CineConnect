from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Logic của bạn ở đây
        self.stdout.write('test')