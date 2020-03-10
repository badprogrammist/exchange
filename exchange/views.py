from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from exchange.models import Currency, Money
from . import service
from .errors import ExchangeError
from .providers import ExchangeRateLoadError
from .serializers import RatesSerializer, ExchangeResultSerializer


def handle_error(view_fun):
    def wrapper(*arg, **kwarg):
        try:
            return view_fun(*arg, **kwarg)
        except ValueError as err:
            return Response(
                data={
                    "message": str(err)
                },
                status=status.HTTP_400_BAD_REQUEST)
        except ExchangeRateLoadError as err:
            return Response(
                data={
                    "message": err.message
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ExchangeError as err:
            return Response(
                data={
                    "message": err.message
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper


@api_view(['GET'])
@handle_error
def rates(request, base_ccy: str):
    base = Currency[base_ccy.upper()]
    rates = service.get_rates(base)
    slz = RatesSerializer(rates)

    return Response(slz.data)


@api_view(['POST'])
@handle_error
def convert(request, base_ccy: str, amount: str, to_ccy: str):
    money = Money.from_str(amount, base_ccy)
    to_ccy_typed = Currency.from_str(to_ccy)
    exch_result = service.convert(money, to_ccy_typed)
    slz = ExchangeResultSerializer(exch_result)
    return Response(slz.data)
