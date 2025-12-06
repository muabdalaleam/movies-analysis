import re

ENV_PATH = "./.env"

def fetch_env(key: str) -> str:
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
