from django.apps import AppConfig


class ExchangeConfig(AppConfig):
    name = 'exchange'
    scheduler_started = False

    def _schedule_rates_updating(self):
        if self.scheduler_started:
            return

        from . import service

        service.schedule_rates_updating()
        self.scheduler_started = True

    def ready(self):
        self._schedule_rates_updating()
