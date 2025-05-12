import os

import hvac

vault_client = hvac.Client(
    url=os.environ.get("ATHENA_VAULT_URL"),
    token=os.environ.get("ATHENA_VAULT_TOKEN"),
)

vault_keys = vault_client.secrets.kv.read_secret_version(
    path=os.environ.get("ATHENA_VAULT_KEY")
)["data"]["data"]

SECRET_KEY = vault_keys["SECRET_KEY"]
DEBUG = int(os.environ.get("DEBUG", 1))
