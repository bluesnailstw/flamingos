from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(every=10,
                                                                   period=IntervalSchedule.MINUTES,
                                                                   )
        PeriodicTask.objects.get_or_create(
            interval=schedule,  # we created this above.
            name='sync_all_host_info',  # simply describes this periodic task.
            task='asset.api.sync_all_host_info',  # name of task.
        )
        print('OK!')
