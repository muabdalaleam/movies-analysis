import re
import time
import requests
from typing import Optional

ENV_PATH = "./.env"

def fetch_env(key: str) -> str:
    """
    My shitty .env parser
    params: a key as a string
    returns: the value of that key as a string always
    """
    with open(ENV_PATH, "r") as f:
        val             = ""
        env_content     = f.read()
        key_value_pairs = re.search(
            r"^\s*(\w+)\s*=\s*\"(.*)\"", env_content
        )

        if not key_value_pairs:
            raise ValueError(f"{ENV_PATH} file in the project root is invalid.")

        key_idx = 1
        while key_idx <= len(key_value_pairs.groups()):
            if key_value_pairs.group(key_idx) == key:
                val = key_value_pairs.group(key_idx+1)
                break

            key_idx += 2

        if not val:
            raise ValueError(f"{val} not found in the {ENV_PATH} file in the root of the project.")

    return val

def retrying_request(url, headers, timeout, max_retries, retry_wait=0,
                     raise_on_fail=True) -> Optional[requests.Response]:
    """
    a request method for paranoid people
    """
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            break
        except (requests.ConnectionError, requests.RequestException) as e:
            retries += 1
            time.sleep(retry_wait)

            print(f"Failed requesting {url} after {retries} retires.")
            if retries >= max_retries:
                if    raise_on_fail: raise e
                else: return None
                

    return response
