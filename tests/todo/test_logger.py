import logging

import pytest

from app.config import LOGGER_NAME
from app.todo import logger


@pytest.mark.parametrize(
    ('message'),
    [
        ('Message'),
    ],
)
def test_logger_success(caplog, message):
    logger.init('test_todo_logs.txt')
    logger.info(message)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'INFO'
    assert message in caplog.text

    assert caplog.record_tuples == [(LOGGER_NAME, logging.INFO, message)]


@pytest.mark.parametrize(
    ('message'),
    [
        (''),
        (None),
    ],
)
def test_logger_fail(caplog, message):
    logger.init('test_todo_logs.txt')
    logger.info(message)

    assert len(caplog.records) == 0
