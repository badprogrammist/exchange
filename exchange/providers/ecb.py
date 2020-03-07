from datetime import datetime

import schema as sm

from .client import HttpClient, ClientError
from .provider import ExchangeRatesProvider, ExchangeRateLoadError
from ..models import Currency, Rate

_POSSIBLE_CCY = [ccy.value for ccy in Currency]

_ccy_validator = sm.Or(*_POSSIBLE_CCY)
_rate_validator = sm.And(sm.Use(float), lambda n: n >= 0)
_date_validator = sm.Regex(r"\d{4}-\d{2}-\d{2}")

_ecb_rate_scm = sm.Schema({
    "rates": {
        _ccy_validator: _rate_validator
    },
    "base": _ccy_validator,
    "date": _date_validator
})


class ECBProvider(ExchangeRatesProvider):
    API_ENDPOINT_CONFIG_NAME = "API_ENDPOINT"

    @classmethod
    def create(cls, endpoint: str):
        if not endpoint:
            raise ValueError("API endpoint is required")

        try:
            client = HttpClient.create()
        except ClientError as err:
            raise ExchangeRateLoadError(
                "Could not create provider"
            ) from err

        return cls(endpoint, client, _ecb_rate_scm)

    @classmethod
    def from_config(cls, settings: dict):
        endpoint = settings[cls.API_ENDPOINT_CONFIG_NAME]
        return cls.create(endpoint)

    def __init__(self,
                 endpoint: str,
                 client: HttpClient,
                 ecb_data_validator: sm.Schema,
                 date_format="%Y-%m-%d"):
        super(ECBProvider, self).__init__()
        self.endpoint = endpoint
        self.client = client
        self.ecb_data_validator = ecb_data_validator
        self.date_format = date_format

    def validate_ecb_data(self, ecb_data):
        """
        Validates dict like:
        {
            "rates": {
                "PLN": 3.8622921348
            },
            "base": "USD",
            "date": "2020-03-04"
        }
        :raise: ExchangeRateLoadError if data is not valid
        """
        if not ecb_data:
            raise ExchangeRateLoadError("Loaded ECB data is null")
        try:
            self.ecb_data_validator.validate(ecb_data)
        except sm.SchemaError as err:
            raise ExchangeRateLoadError(
                "Loaded ECB data is invalid"
            ) from err

    def build_rate(self,
                   from_ccy: Currency,
                   to_ccy: Currency,
                   ecb_data: dict) -> Rate:
        self.validate_ecb_data(ecb_data)

        rate = ecb_data["rates"][to_ccy.value]
        try:
            dt = datetime.strptime(ecb_data["date"], self.date_format)
        except ValueError as err:
            raise ExchangeRateLoadError(
                "Date is not invalid"
            ) from err

        return Rate(
            from_ccy=from_ccy,
            to_ccy=to_ccy,
            value=rate,
            dt=dt
        )

    async def load_rate(self,
                        from_ccy: Currency,
                        to_ccy: Currency) -> Rate:
        if not from_ccy:
            raise ValueError("Base currency is required")

        if not to_ccy:
            raise ValueError("Exchange currency is required")

        params = {"base": from_ccy.value,
                  "symbols": to_ccy.value}

        try:
            ecb_data = await self.client.get_json(self.endpoint,
                                                  params)
            return self.build_rate(from_ccy,
                                   to_ccy,
                                   ecb_data)

        except ClientError as err:
            raise ExchangeRateLoadError(
                "Could not load rates."
            ) from err

    async def release_resource(self):
        await self.client.release_resources()
