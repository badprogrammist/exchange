from django.db import models

from enum import Enum


class Currency(Enum):
    CZK = "CZK"
    EUR = "EUR"
    PLN = "PLN"
    USD = "USD"


