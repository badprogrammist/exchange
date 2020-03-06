from environs import Env

env = Env()
env.read_env()

PG_HOST = env.str("PG_HOST")
PG_PORT = env.int("PG_PORT", default=5432)
PG_NAME = env.str("PG_NAME")
PG_USER = env.str("PG_USER")
PG_PASS = env.str("PG_PASS")

EXCHANGE_DATA_PROVIDER = env.str("EXCHANGE_DATA_PROVIDER",
                                 default="ECB_PROVIDER")

ECB_PROVIDER_API_ENDPOINT = env.str("ECB_PROVIDER_API_ENDPOINT",
                                    default="https://exchangeratesapi.io/")
