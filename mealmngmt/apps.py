from django.apps import AppConfig


class MealmngmtConfig(AppConfig):
    name = 'mealmngmt'

    def ready(self):
        print("HUUUUUUUUUUUUUUUUUu")
        from scheduler import scheduler
        scheduler.start()
