from rest_framework import serializers as slz

from exchange.models import Currency


class RatesSerializer(slz.Serializer):
    dt = slz.DateTimeField()
    base = slz.ChoiceField(Currency.choices)
    rates = slz.DictField()


class ExchangeResultSerializer(slz.Serializer):
    dt = slz.DateTimeField()
    currency = slz.ChoiceField(Currency.choices, source="money.ccy")
    amount = slz.DecimalField(max_digits=20,
                              decimal_places=10,
                              source="money.amount")
