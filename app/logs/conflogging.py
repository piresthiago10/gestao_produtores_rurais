from app.config import LOGGING_CONFIG
from logging.config import dictConfig


def setup_logging():
    """Configura os logs para a aplicação."""
    dictConfig(LOGGING_CONFIG)
