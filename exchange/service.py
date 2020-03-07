import asyncio
import itertools as it
import typing

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction

from .models import Currency, Rate
from .providers import create_provider
import logging


def load_rates() -> typing.List[Rate]:
    async def load_async():
        try:
            provider_name = settings.EXCHANGE_DATA_PROVIDER_NAME
            provider_settings = settings.EXCHANGE_DATA_PROVIDER_SETTINGS
            provider = create_provider(provider_name, provider_settings)
        except ValueError as err:
            raise ImproperlyConfigured(
                "Invalid settings for provider."
            ) from err

        async with provider as p:
            ccy_pairs = it.permutations(Currency, 2)
            futures = [p.load_rate(from_ccy, to_ccy)
                       for from_ccy, to_ccy in ccy_pairs]
            return await asyncio.gather(*futures)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rates = loop.run_until_complete(load_async())
    return rates


@transaction.atomic
def save_rates(rates: typing.List[Rate]):
    Rate.objects.all().delete()
    Rate.objects.bulk_create(rates)


def update_rates():
    logging.info("Start update exchange rates")
    rates = load_rates()
    save_rates(rates)
    logging.info("Exchange rates updated successfully")


def schedule_rates_updating():
    scheduler = BackgroundScheduler()
    seconds = settings.EXCHANGE_RATES_UPDATE_INTERVAL_SEC
    scheduler.add_job(update_rates,
                      id="rates_updater",
                      replace_existing=True,
                      trigger='interval',
                      seconds=seconds)
    scheduler.start()
