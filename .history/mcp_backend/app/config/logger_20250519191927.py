import logging
from logging.config import dictConfig

def setup_logger():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/bmhe.log",
                "formatter": "default",
                "level": "INFO",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    }

    dictConfig(logging_config)


# Call this early (ex: main.py or Alembic env.py)
setup_logger()

# Shortcut for use
logger = logging.getLogger("bmhe")