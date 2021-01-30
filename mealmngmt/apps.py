from django.apps import AppConfig


class MealmngmtConfig(AppConfig):
    name = 'mealmngmt'

    def ready(self):
        from scheduler import scheduler
        scheduler.start()
