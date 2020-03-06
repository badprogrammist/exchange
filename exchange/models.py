from decimal import Decimal

from django.db import models

from enum import Enum
import datetime


class Currency(Enum):
    CZK = "CZK"
    EUR = "EUR"
    PLN = "PLN"
    USD = "USD"


class Rate(models.Model):
    from_ccy: Currency
    to_ccy: Currency
    value: Decimal
    dt: datetime.datetime
