import logging
import logging.config
import os

from src.ai_nutritionist.settings import settings

os.makedirs(settings.ERROR_LOGGING_PATH, exist_ok=True)
error_log_file_path = os.path.join(settings.ERROR_LOGGING_PATH, "logs")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] [%(levelname)s] - %(message)s (%(filename)s:%(lineno)s)",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "stream": "ext://sys.stdout",
        },
        "error_log_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "verbose",
            "filename": error_log_file_path,
            "mode": "a",
            "maxBytes": 5 * 1024 * 1024,  # 5MB max log size
            "backupCount": 3,  # Keep last 3 log files
        },
    },
    "loggers": {
        "ai_nutritionist": {
            "handlers": ["console", "error_log_file_handler"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)
