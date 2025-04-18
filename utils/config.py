import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../data/config.json")


def get_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def get_debug_mode():
    return get_config().get("debug", False)


def set_debug_mode(state: bool):
    config = get_config()
    config["debug"] = state
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
