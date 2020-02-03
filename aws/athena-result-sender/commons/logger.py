import logging
from sys import stdout


def config_log():
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)
    handler = logging.StreamHandler(stdout)
    handler.setFormatter(logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
