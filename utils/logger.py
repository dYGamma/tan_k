# utils/logger.py
import logging
import logging.config
import sys

def setup_logging(config_path: str):
    """Загружает настройки логирования из файла .ini."""
    logging.config.fileConfig(
        config_path,
        defaults={'sys': sys},
        disable_existing_loggers=False
    )