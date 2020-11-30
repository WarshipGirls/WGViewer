import sys
import time
import logging
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout, QApplication

logger = logging.getLogger(__name__)


class ConsoleWindowLogHandler(logging.Handler, QObject):
    sigLog = pyqtSignal(str)
    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, logRecord):
        message = str(logRecord.getMessage())
        self.sigLog.emit(message)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        # Layout
        textBox = QTextEdit()
        textBox.setReadOnly(True)
        self.button = QPushButton('Click')
        self.button2 = QPushButton('Interrupt')
        vertLayout = QVBoxLayout()
        vertLayout.addWidget(textBox)
        vertLayout.addWidget(self.button)
        vertLayout.addWidget(self.button2)
        self.setLayout(vertLayout)

        # Connect button
        #self.button.clicked.connect(self.someProcess) # blocking
        self.button.clicked.connect(self.buttonPressed)
        self.button2.clicked.connect(self.interrupt)
        # Thread
        self.bee = Worker(self.someProcess, ())
        self.bee.finished.connect(self.restoreUi)
        self.bee.terminate()

        # Console handler
        consoleHandler = ConsoleWindowLogHandler()
        consoleHandler.sigLog.connect(textBox.append)
        logger.addHandler(consoleHandler)

    def interrupt(self):
        logger.error("aslkdfjasl;kdfja;sldkjf")

    def buttonPressed(self):
        self.button.setEnabled(False)
        self.bee.start()

    def someProcess(self):
        logger.error("starting")
        for i in range(10):
            logger.error("line%d" % i)
            time.sleep(1)

    def restoreUi(self):
        self.button.setEnabled(True)


class Worker(QThread):
    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()