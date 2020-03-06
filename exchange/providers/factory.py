from .ecb import ECBProvider
from .provider import ExchangeRatesProvider

ECB_PROVIDER_NAME = "ECB_PROVIDER"


def create_provider(name, config) -> ExchangeRatesProvider:
    if not name:
        raise ValueError("Provider name is null")

    if not config:
        raise ValueError("Config is null")

    if name == ECB_PROVIDER_NAME:
        return ECBProvider.from_config(config)

    raise ValueError(f"Unsupported provider: {name}")
