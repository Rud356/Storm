import logging
from .app_logger import app_logger
from .events_logger import events_logger

logging.basicConfig( # noqa: pycharm doesn't understands this function.
    format="%(name)s %(levelno)s %(asctime)s: %(message)s",
    level=logging.DEBUG
)
