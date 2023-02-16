import json
from pathlib import Path
BASE_DIR = Path(__file__).parent
default_value: str|None = None,
def get_secret(
    key:str,
    json_path: str = str(BASE_DIR/"secrets.json")
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")

db_url = get_secret("db_url")
slack_token = get_secret("slack_token")
openapi_key = get_secret("openapi_key")