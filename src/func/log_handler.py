import logging

from typing import Callable

from PyQt5.QtCore import QObject, pyqtSignal

from src.utils import get_curr_time


class LogHandler(logging.Handler, QObject):
    sig_log = pyqtSignal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, log_record: logging.LogRecord) -> None:
        msg = f"{get_curr_time()} - " + str(log_record.getMessage())
        self.sig_log.emit(msg)


def get_new_logger(name: str, level: int, signal: Callable = None) -> logging.Logger:
    logger = logging.getLogger(name)
    log_handler = LogHandler()
    if signal is not None:
        log_handler.sig_log.connect(signal)
    else:
        pass
    logger.addHandler(log_handler)
    log_handler.setLevel(level=level)
    return logger


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

# End of File
