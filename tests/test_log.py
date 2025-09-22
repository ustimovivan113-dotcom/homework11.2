import pytest
import logging


def test_log_setup():
    logger = logging.getLogger("test")
    assert logger.level == logging.DEBUG


def test_log_message():
    logger = logging.getLogger("test")
    logger.info("Test message")
    assert True


def test_log_error():
    logger = logging.getLogger("test")
    with pytest.raises(Exception):
        logger.error("Test error")
        raise Exception("Error for testing")
