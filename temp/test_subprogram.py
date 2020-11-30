import sys

# On Windows it looks like cp850 is used for my console. We need it to decode the QByteArray correctly.
# Based on https://forum.qt.io/topic/85064/qbytearray-to-string/2
import ctypes

#The QProcess class is used to start external programs and to communicate with them

CP_console = "cp" + str(ctypes.cdll.kernel32.GetConsoleOutputCP())

from PyQt5 import QtCore, QtGui, QtWidgets


class gui(QtWidgets.QMainWindow):
    def __init__(self):
        super(gui, self).__init__()
        self.initUI()

    def dataReady(self):
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.End)

        # Here we have to decode the QByteArray
        cursor.insertText(str(self.process.readAll().data().decode(CP_console)))
        #self.output.ensureCursorVisible()

    def callProgram(self):
        # run the process
        # `start` takes the exec and a list of arguments
        self.process.start('ping', ['127.0.0.1'])

    def initUI(self):
        # Layout are better for placing widgets
        layout = QtWidgets.QVBoxLayout()
        self.runButton = QtWidgets.QPushButton('Run')
        self.runButton.clicked.connect(self.callProgram)

        #self.output = QtWidgets.QTextEdit()
        self.output = QtWidgets.QTextBrowser()
        self.output.setReadOnly(True)

        layout.addWidget(self.output)
        layout.addWidget(self.runButton)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyRead.connect(self.dataReady)

        # Just to prevent accidentally running multiple times
        # Disable the button when process starts, and enable it when it finishes
        self.process.started.connect(lambda: self.runButton.setEnabled(False))
        self.process.finished.connect(lambda: self.runButton.setEnabled(True))


# Function Main Start
def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = gui()
    ui.show()
    sys.exit(app.exec_())


# Function Main END

if __name__ == '__main__':
    main()
