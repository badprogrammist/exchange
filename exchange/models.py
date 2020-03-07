from django.db import models


class Currency(models.TextChoices):
    CZK = "CZK"
    EUR = "EUR"
    PLN = "PLN"
    USD = "USD"


class Rate(models.Model):
    class Meta:
        unique_together = (('from_ccy', 'to_ccy'),)

    from_ccy = models.CharField(max_length=3,
                                choices=Currency.choices)
    to_ccy = models.CharField(max_length=3,
                              choices=Currency.choices)
    value = models.DecimalField(max_digits=10, decimal_places=5)
    dt = models.DateTimeField()
