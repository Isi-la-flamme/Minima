import logging
from minima.core.logger import get_logger

def test_logger_creation():
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)

def test_logger_output(caplog):
    logger = get_logger("test_logger_output")
    with caplog.at_level(logging.INFO):
        logger.info("message de test")
    assert any("message de test" in rec.message for rec in caplog.records)
