"""JWT Helper"""

import copy
import json
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

import time
from typing import Dict
import anfler.util.log.lw as lw

# ---------------------------------------------------------------------------
#   Global objects
# ---------------------------------------------------------------------------
_log = lw.get_logger("anfler.util.jwt")

JWT_CONFIG={
    "PUBLIC_KEY":None,
    "PUBLIC_KEY_FILE":None,
    "PRIVATE_KEY": None,
    "PRIVATE_KEY_FILE": None,
    "PRIVATE_PASS":None,
    "ALGORITHM": "RS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 1
}   # JWT configuration


def __load_key(filename):
    try:
        with open(filename, 'rb') as fd:
            return fd.read()
    except Exception as e:
        #raise Exception(f'Cannot load key from file {filename}. {str(e)}')
        _log.error(f'Cannot load key from file {filename}. {str(e)}')
        assert False, f'Cannot load key from file {filename}. {str(e)}'

def jwt_load_config(filename):
    """Load JWT settings
    :param filename: Json configuration
    """
    global  JWT_CONFIG
    try:
        with open(filename) as json_file:
            jwt_set_config(json.load(json_file))

    except Exception as e:
        _log.error( f"Cannot open/read JWT configuration file '{filename}':  {(str(e))}")
        assert bool(JWT_CONFIG), f"Cannot open/read JWT configuration file '{filename}':  {(str(e))}"

    assert JWT_CONFIG.get("PUBLIC_KEY") is None , f"JWT_CONFIG invalid: missing PUBLIC_KEY/PUBLIC_KEY_FILE or SECRET_KEY"


def jwt_set_config(config:Dict):
    """Set JWT settings
    :param config: JWT configuration
    """
    global JWT_CONFIG
    JWT_CONFIG = config.copy()
    if JWT_CONFIG.get("PUBLIC_KEY_FILE", None) is not None:
        JWT_CONFIG["PUBLIC_KEY"] = __load_key(JWT_CONFIG["PUBLIC_KEY_FILE"])
    if JWT_CONFIG.get("PRIVATE_KEY_FILE", None) is not None:
        JWT_CONFIG["PRIVATE_KEY"] = (__load_key(JWT_CONFIG["PRIVATE_KEY_FILE"])).decode("utf-8")
        if JWT_CONFIG.get("PRIVATE_PASS", None) is not None:
            pem_bytes = JWT_CONFIG["PRIVATE_KEY"].encode()
            # load to test
            _ = serialization.load_pem_private_key(pem_bytes, password=JWT_CONFIG["PRIVATE_PASS"].encode(), backend=default_backend())

def jwt_encode(payload: dict) -> Dict[str, str]:
    """Encode dict using JWT
    :param payload: dictionary to encode

    :return Encoded payload
    """
    global  JWT_CONFIG
    payload2 = copy.deepcopy(payload)
    payload2["exp"] = time.time() + (int(JWT_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"]) * 60)
    if JWT_CONFIG.get("PRIVATE_PASS", None) is not None:
        private_key = serialization.load_pem_private_key(str.encode(JWT_CONFIG["PRIVATE_KEY"]), password=str.encode(JWT_CONFIG["PRIVATE_PASS"]), backend=default_backend())
    else:
        private_key = str.encode(JWT_CONFIG["PRIVATE_KEY"])

    token = jwt.encode(payload2, private_key, algorithm=JWT_CONFIG["ALGORITHM"])
    return token

def jwt_decode(token: str) -> dict:
    """Decode token string
    :param token: Encoded payload

    :return Decoded token (Dic) or {} if token expired or is invalid
    """
    global JWT_CONFIG
    try:
        decoded_token = jwt.decode(token, JWT_CONFIG["PUBLIC_KEY"], algorithms=[JWT_CONFIG["ALGORITHM"]])
        if decoded_token["exp"] >= time.time():
            return decoded_token
        else:
            return {}
    except Exception as e:
        _log.error(f'Cannot decode token: {str(e)}')
        return {}


