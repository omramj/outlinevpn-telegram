import codecs
import json
import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from requests import Response
from amnezia import warp_api

from helpers.classes import TextKey


def generate_amnezia_key(type: str = "amnezia-warp", keyname: str = "TODO") -> TextKey:

    if type == "amnezia-warp":
        amnezia_config_plaintext = _create_warp_config()
        kid = "amnezia-warp"
        server_id = "warp"
    else:
        #TODO
        raise Exception

    awg_config_base64 = _encode_base64(amnezia_config_plaintext)

    key = TextKey(type=type,
                  kid=kid,
                  name=keyname,
                  access_string=awg_config_base64,
                  server_id=server_id)

    return key


def _create_warp_config() -> str:

    wg_privkey, wg_pubkey = _generate_wg_key_pair()

    api_response = warp_api.generate_config(wg_pubkey)

    wg_conn_data = _parse_warp_api_response(api_response)

    awg_config_plaintext = _compose_awg_warp_config(wg_privkey, wg_conn_data)


    return awg_config_plaintext 



def _encode_base64(plaintext: str) -> str:
    plaintext_bytes = plaintext.encode("utf8")
    bs64 = base64.b64encode(plaintext_bytes)

    return bs64.decode("utf8")



def _compose_awg_warp_config(wg_privkey: str, wg_conn_data: dict) -> str:
    config = f"""
[Interface]
PrivateKey = {wg_privkey}
S1 = 0
S2 = 0
Jc = 120
Jmin = 23
Jmax = 911
H1 = 1
H2 = 2
H3 = 3
H4 = 4
MTU = 1280
Address = {wg_conn_data.get("client_ipv4")}, {wg_conn_data.get("client_ipv6")}
DNS = 1.1.1.1, 2606:4700:4700::1111, 1.0.0.1, 2606:4700:4700::1001

[Peer]
PublicKey = {wg_conn_data.get("peer_pubkey")}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = 188.114.97.66:3138
"""
    return config


def _parse_warp_api_response(response: Response) -> dict:
    response_json = json.loads(response.text)
    result = response_json.get("result")
    data = {
            "peer_pubkey": result.get("config").get("peers")[0].get("public_key"),
            "client_ipv4": result.get("config").get("interface").get("addresses").get("v4"),
            "client_ipv6": result.get("config").get("interface").get("addresses").get("v6")
            }

    return data


def _generate_wg_key_pair() -> tuple:

    private_key = X25519PrivateKey.generate()

    private_bytes = private_key.private_bytes(  
        encoding=serialization.Encoding.Raw,  
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_bytes = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
            )

    private_str = codecs.encode(private_bytes, 'base64').decode('utf8').strip()
    public_str = codecs.encode(public_bytes, 'base64').decode('utf8').strip()

    return (private_str, public_str)
