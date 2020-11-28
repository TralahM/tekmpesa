from mpesa.ghana import API
import yaml
import os

secret_file = os.path.expanduser("~/.openapi_mpesaportal.secrets.yml")
with open(secret_file, "r") as rf:
    secrets = yaml.load(rf, Loader=yaml.Loader)

public_key = secrets.get("sandbox_public_key")
api_key = secrets.get("sandbox_api_key")
env = "sandbox"

api = API(public_key=public_key, api_key=api_key, env=env)
# print(f"api.session_id = {api.session_id}")
