from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QScrollArea, QMainWindow, QApplication

from src.utils.wgv_pyqt import get_user_resolution


class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)


class ScrollBoxWindow(QMainWindow):
    sig_close = pyqtSignal()

    def __init__(self, parent, title, text):
        super().__init__()
        self.setWindowTitle(title)
        user_w, user_h = get_user_resolution()
        self.w = int(user_w * 0.3)
        self.h = int(self.w * 0.618)
        label = ScrollLabel(self)
        label.setText(text)
        # TODO? use setContentMargins to fill the window; instead of setGeometry (inelegant)
        label.setGeometry(0, 0, self.w, self.h)
        self.resize(self.w, self.h)
        self.center()
        self.sig_close.connect(parent.delete_version_log)

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def closeEvent(self, e: QCloseEvent) -> None:
        self.sig_close.emit()


# End of File
