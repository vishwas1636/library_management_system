from django.apps import AppConfig

class LibraryManagementConfig(AppConfig):
    name = 'library_management'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1, period=IntervalSchedule.DAYS
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name="Send Overdue Remainders",
            task="library_management.tasks.send_overdue_remainders",
        )
