import logging
from logging.config import dictConfig
from utils.load_config import load_config
from pathlib import Path


class Logging:
    def __init__(self, name):
        log_dict = load_config(Path(__file__).parent / "config/log.yaml")
        Path(log_dict["handlers"]["info_file_handler"]["filename"]).parent.mkdir(
            parents=True, exist_ok=True
        )
        dictConfig(log_dict)
        self.logger = logging.getLogger(name)