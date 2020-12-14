from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent, QColor, QPalette
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QScrollArea, QMainWindow, QApplication, QFrame

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

    def setText(self, text) -> None:
        self.label.setText(text)


class ScrollBoxWindow(QMainWindow):
    sig_close = pyqtSignal()

    def __init__(self, parent, title: str, text: str):
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

    def center(self) -> None:
        frame_gm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def closeEvent(self, e: QCloseEvent) -> None:
        self.sig_close.emit()


class QCustomLine(QFrame):
    def __init__(self, parent, color: QColor, width: int):
        super().__init__(parent)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(width)
        self.setMidLineWidth(0)
        self.setContentsMargins(0, 0, 0, 0)
        # setColor works when there is no default QSS
        self.setColor(color)
        # following is a workaround for QSS=qdarkstyle
        self.setStyleSheet('QFrame { background-color: white }')

    def setColor(self, color) -> None:
        pal = self.palette()
        pal.setColor(QPalette.WindowText, color)
        self.setPalette(pal)


class QHLine(QCustomLine):
    def __init__(self, parent=None, color=QColor(Qt.black), width=10):
        super().__init__(parent, color, width)
        self.setFrameShape(QFrame.HLine)
        self.setObjectName('horizontal_line')


class QVLine(QCustomLine):
    def __init__(self, parent=None, color=QColor(Qt.black), width=10):
        super().__init__(parent, color)
        self.setFrameShape(QFrame.VLine)
        self.setObjectName('vertical_line')

# End of File
