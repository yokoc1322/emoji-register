from __future__ import annotations

import logging

LOGGER_NAME = "emoji_register.server"


def get_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(LOGGER_NAME)
    return logger
