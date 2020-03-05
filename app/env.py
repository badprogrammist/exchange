from environs import Env

env = Env()
env.read_env()

PG_HOST = env.str("PG_HOST")
PG_PORT = env.int("PG_PORT", default=5432)
PG_NAME = env.str("PG_NAME")
PG_USER = env.str("PG_USER")
PG_PASS = env.str("PG_PASS")

EXCHANGE_DATA_PROVIDER = env.str("EXCHANGE_DATA_PROVIDER",
                                 default="OPEN_EXCHANGE_RATES")

OPEN_EXCHANGE_RATES_APP_ID = env.str("OPEN_EXCHANGE_RATES_APP_ID")
OPEN_EXCHANGE_RATES_ENDPOINT = env.str("OPEN_EXCHANGE_RATES_ENDPOINT",
                                       default="https://docs.openexchangerates.org/")
