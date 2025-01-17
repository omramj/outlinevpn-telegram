
import requests
import datetime
import json


api="https://api.cloudflareclient.com/v0i1909051800/reg"


def generate_config(wg_pubkey: str) -> requests.Response:

    tos = str(datetime.datetime.now(datetime.timezone.utc).isoformat()).replace('+00:00', 'Z')

    headers = {
            "user-agent": "",
            "content-type": "application/json",
            }

    data = {
            "install_id": "",
            "tos": tos,
            "key": wg_pubkey,
            "fcm_token": "",
            "type": "ios",
            "locale": "en_US"
            }

    r = requests.post(api, data = json.dumps(data), headers=headers)

    return r
