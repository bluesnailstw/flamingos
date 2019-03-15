from django.core.management.base import BaseCommand, CommandError
from asset.tasks import sync_all_host_info


class Command(BaseCommand):
    def handle(self, *args, **options):
        async_task = sync_all_host_info.delay()
        print('celery async id: %s' % async_task.id)
