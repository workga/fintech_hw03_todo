import logging

from app.config import LOGGER_FILENAME, LOGGER_NAME


def init(filename: str = LOGGER_FILENAME) -> None:
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(
        logging.Formatter(
            '%(levelname)s %(asctime)s %(funcName)s(%(lineno)d) %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
        )
    )

    tasks_logger = logging.getLogger(LOGGER_NAME)
    tasks_logger.addHandler(file_handler)
    tasks_logger.setLevel(logging.INFO)


def info(message: str) -> None:
    if message:
        logging.getLogger(LOGGER_NAME).info(message)
