import logging

from PyQt5.QtCore import QObject, pyqtSignal


class LogHandler(logging.Handler, QObject):
    sig_log = pyqtSignal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, log_record):
        msg = str(log_record.getMessage())
        self.sig_log.emit(msg)

# End of File
