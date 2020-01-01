import functools
import json

from chat_commands import vote_fun


def load_config(file):
    config = None
    with open(file) as f:
        config = json.load(f)
    return config


def create_config(config_file):
    command = {}
    for key, value in config_file["commands"].items():
        command[key] = functools.partial(vote_fun, vote=value)
    command["!pause"] = functools.partial(vote_fun, vote="secret_pause")
    command["!run"] = functools.partial(vote_fun, vote="secret_run")
    return command
