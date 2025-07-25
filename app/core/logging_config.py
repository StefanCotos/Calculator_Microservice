import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a logger with the specified name.
    The logger is configured to output log messages
        to the standard output stream
    using a specific format that includes the timestamp,
        log level, logger name, and message.
    If the logger does not already have handlers, a StreamHandler is added.
    Args:
        name (str): The name of the logger to create or retrieve.
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
