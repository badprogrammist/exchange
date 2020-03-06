from abc import ABC, abstractmethod

from exchange.models import Currency, Rate


class ExchangeRateLoadError(Exception):
    pass


class ExchangeRatesProvider(ABC):
    """
    Base class for services that provides actual exchange rates data
    """

    @abstractmethod
    async def load_rate(self, from_ccy: Currency, to_ccy: Currency) -> Rate:
        """
        Loads exchange rate for given currencies
        :param from_ccy: Change base currency
        :param to_ccy: Exchange rate currency
        :return: Rate object
        """
        raise NotImplementedError

    @abstractmethod
    async def release_resource(self):
        """
        Optional. Releases acquired resources
        """
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release_resource()
