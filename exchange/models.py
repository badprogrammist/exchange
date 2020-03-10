from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.db import models


class Currency(models.TextChoices):
    CZK = "CZK"
    EUR = "EUR"
    PLN = "PLN"
    USD = "USD"

    @classmethod
    def from_str(cls, ccy: str):
        if not ccy or ccy not in Currency:
            raise ValueError("Currency is invalid")

        return Currency[ccy.upper()]


class Money:
    # TODO Support iso4217
    # TODO Consider different currency exponents
    ccy_fractions = {
        Currency.CZK: '.01',
        Currency.EUR: '.01',
        Currency.PLN: '.01',
        Currency.USD: '.01',
    }

    @classmethod
    def from_str(cls, amount: str, ccy: str):
        ccy_typed = Currency.from_str(ccy)

        try:
            amount_typed = Decimal(amount)
        except (TypeError, InvalidOperation) as err:
            raise ValueError(
                "Amount is invalid"
            ) from err

        return cls(amount_typed, ccy_typed)

    def __init__(self, amount: Decimal, ccy: Currency):
        self.amount = amount
        self.ccy = ccy

    # TODO Add supporting +, -, % operations

    def round(self) -> Decimal:
        fraction = Decimal(self.ccy_fractions[self.ccy])
        return self.amount.quantize(fraction, ROUND_HALF_UP)


class Rate(models.Model):
    class Meta:
        unique_together = (('from_ccy', 'to_ccy'),)

    from_ccy = models.CharField(max_length=3,
                                choices=Currency.choices)
    to_ccy = models.CharField(max_length=3,
                              choices=Currency.choices)

    # TODO max_digits=20, decimal_places=10
    value = models.DecimalField(max_digits=20, decimal_places=10)
    dt = models.DateTimeField()

    def convert(self, money: Money) -> Money:
        if not money or money.ccy != self.from_ccy:
            raise ValueError(
                f"Cannot convert money of currency {money.ccy.value}")

        return Money(self.value * money.amount, Currency[self.to_ccy])


@dataclass
class Rates:
    dt: datetime
    base: Currency
    rates: dict


@dataclass
class ExchangeResult:
    dt: datetime
    money: Money
