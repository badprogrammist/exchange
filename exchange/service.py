import asyncio
import itertools as it
import logging
import typing
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction

from .errors import ExchangeError
from .models import (Currency, Rate, Money,
                     Rates, ExchangeResult)
from .providers import create_provider


def convert(money: Money, to_ccy: Currency) -> ExchangeResult:
    if money.ccy == to_ccy:
        return ExchangeResult(datetime.now(),
                              money)

    rate = Rate.objects.get(from_ccy=money.ccy,
                            to_ccy=to_ccy)
    if not rate:
        raise ExchangeError(
            f"There is no rate for currencies"
            f" {money.ccy.value}:{to_ccy.value}")

    converted_money = rate.convert(money)
    return ExchangeResult(rate.dt, converted_money)


def get_rates(base: Currency) -> Rates:
    rates = Rate.objects.filter(from_ccy=base)

    assert (len({rate.dt for rate in rates}) == 1,
            "Rates have different dt")

    dt = rates[0].dt
    return Rates(
        dt,
        base,
        {rate.to_ccy: rate.value
         for rate in rates}
    )


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
    if not rates:
        raise ValueError("Attempt to save empty rates")
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
                      seconds=seconds,
                      next_run_time=datetime.now())
    scheduler.start()
