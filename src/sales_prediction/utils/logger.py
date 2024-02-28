import logging
from logging.config import dictConfig
from pathlib import Path


class Logging:
    def __init__(self, name: str, log_dict: dict):
        """
        Initializes the Logging class.

        Args:
            name (str): the name of the logger
            log_dict (dict): the log dict
        """
        Path(log_dict["handlers"]["info_file_handler"]["filename"]).parent.mkdir(
            parents=True, exist_ok=True
        )
        dictConfig(log_dict)
        self.logger = logging.getLogger(name)
