from .ecb import ECBProvider
from .provider import ExchangeRatesProvider

ECB_PROVIDER_NAME = "ECB_PROVIDER"


def create_provider(name, settings) -> ExchangeRatesProvider:
    if not name:
        raise ValueError("Provider name is null")

    if not settings:
        raise ValueError("Config is null")

    if name == ECB_PROVIDER_NAME:
        if name not in settings:
            raise ValueError(f"There are not settings for {name} provider.")

        return ECBProvider.from_config(settings[name])

    raise ValueError(f"Unsupported provider: {name}")
