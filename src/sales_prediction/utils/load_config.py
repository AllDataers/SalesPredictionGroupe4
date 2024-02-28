import yaml
from typing import Union
from pathlib import Path


def load_config(config_path: Union[str, Path]) -> dict:
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config
