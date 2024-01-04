import logging

from logging.config import dictConfig
from logging import Logger, getLogger
from rich.logging import RichHandler

# Logger
logging_config = dict(
        version = 1,
        formatters = {
            'f': {
                    'format': '%(levelname)s - %(asctime)s - %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
        },
        handlers = {
            'h': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'f',
                    'level': logging.DEBUG
                }
        },
        root = {
            'handlers': ['h'],
            'level': logging.DEBUG,
        },
    )

def get_root_logger() -> None:
    """
    Returns a logger object with the specified logging level.
    """
    logger = getLogger()
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])

    handler = RichHandler(markup=True)
    logger.addHandler(handler)


def create_logger(name: str) -> Logger:
    """Creatte a logger with requested name."""

    dictConfig(logging_config)
    logger = logging.getLogger()

    return logger
