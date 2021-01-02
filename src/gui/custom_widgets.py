from math import ceil

from PyQt5.QtCore import Qt, pyqtSignal, QTimer, pyqtSlot, QRect
from PyQt5.QtGui import QCloseEvent, QColor, QPalette, QPainter
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QScrollArea, QMainWindow, QApplication, QFrame

from src.utils import get_user_resolution


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()


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
        super().__init__(parent, color, width)
        self.setFrameShape(QFrame.VLine)
        self.setObjectName('vertical_line')


class QtWaitingSpinner(QWidget):
    # https://stackoverflow.com/questions/48441863/is-there-a-way-to-implement-a-circular-waiting-indicator-using-pyqt
    mColor = QColor(Qt.gray)
    mRoundness = 100.0
    mMinimumTrailOpacity = 31.4159265358979323846
    mTrailFadePercentage = 50.0
    mRevolutionsPerSecond = 1.57079632679489661923
    mNumberOfLines = 20
    mLineLength = 10
    mLineWidth = 2
    mInnerRadius = 20
    mCurrentCounter = 0
    mIsSpinning = False

    def __init__(self, center_on_parent=True, disable_parent_when_spinning=True, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.mCenterOnParent = center_on_parent
        self.mDisableParentWhenSpinning = disable_parent_when_spinning

        self.timer = None
        self.initialize()

    def initialize(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()

    @pyqtSlot()
    def rotate(self):
        self.mCurrentCounter += 1
        if self.mCurrentCounter > self.numberOfLines():
            self.mCurrentCounter = 0
        self.update()

    def updateSize(self):
        size = (self.mInnerRadius + self.mLineLength) * 2
        self.setFixedSize(size, size)

    def updateTimer(self):
        self.timer.setInterval(1000 / (self.mNumberOfLines * self.mRevolutionsPerSecond))

    def updatePosition(self):
        if self.parentWidget() and self.mCenterOnParent:
            _x = int(self.parentWidget().width() / 2 - self.width() / 2)
            _y = int(self.parentWidget().height() / 2 - self.height() / 2)
            self.move(_x, _y)

    @staticmethod
    def lineCountDistanceFromPrimary(current, primary, total_lines):
        distance = primary - current
        if distance < 0:
            distance += total_lines
        return distance

    def currentLineColor(self, count_distance, total_lines, trail_fade_percent, min_opacity, color):
        if count_distance == 0:
            return color

        min_alpha_f = min_opacity / 100.0

        distance_threshold = ceil((total_lines - 1) * trail_fade_percent / 100.0)
        if count_distance > distance_threshold:
            color.setAlphaF(min_alpha_f)

        else:
            alpha_diff = self.mColor.alphaF() - min_alpha_f
            gradient = alpha_diff / distance_threshold + 1.0
            result_alpha = color.alphaF() - gradient * count_distance
            result_alpha = min(1.0, max(0.0, result_alpha))
            color.setAlphaF(result_alpha)
        return color

    def paintEvent(self, event):
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)
        if self.mCurrentCounter > self.mNumberOfLines:
            self.mCurrentCounter = 0
        painter.setPen(Qt.NoPen)

        for i in range(self.mNumberOfLines):
            painter.save()
            painter.translate(self.mInnerRadius + self.mLineLength,
                              self.mInnerRadius + self.mLineLength)
            rotate_angle = 360.0 * i / self.mNumberOfLines
            painter.rotate(rotate_angle)
            painter.translate(self.mInnerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(i, self.mCurrentCounter,
                                                         self.mNumberOfLines)
            color = self.currentLineColor(distance, self.mNumberOfLines,
                                          self.mTrailFadePercentage, self.mMinimumTrailOpacity, self.mColor)
            painter.setBrush(color)
            painter.drawRoundedRect(QRect(0, -self.mLineWidth // 2, self.mLineLength, self.mLineLength),
                                    self.mRoundness, Qt.RelativeSize)
            painter.restore()

    def start(self):
        self.updatePosition()
        self.mIsSpinning = True
        self.show()

        if self.parentWidget() and self.mDisableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self.timer.isActive():
            self.timer.start()
            self.mCurrentCounter = 0

    def stop(self):
        self.mIsSpinning = False
        self.hide()

        if self.parentWidget() and self.mDisableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self.timer.isActive():
            self.timer.stop()
            self.mCurrentCounter = 0

    def setNumberOfLines(self, lines):
        self.mNumberOfLines = lines
        self.updateTimer()

    def setLineLength(self, length):
        self.mLineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self.mLineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self.mInnerRadius = radius
        self.updateSize()

    def color(self):
        return self.mColor

    def roundness(self):
        return self.mRoundness

    def minimumTrailOpacity(self):
        return self.mMinimumTrailOpacity

    def trailFadePercentage(self):
        return self.mTrailFadePercentage

    def revolutionsPersSecond(self):
        return self.mRevolutionsPerSecond

    def numberOfLines(self):
        return self.mNumberOfLines

    def lineLength(self):
        return self.mLineLength

    def lineWidth(self):
        return self.mLineWidth

    def innerRadius(self):
        return self.mInnerRadius

    def isSpinning(self):
        return self.mIsSpinning

    def setRoundness(self, roundness):
        self.mRoundness = min(0.0, max(100, roundness))

    def setColor(self, color):
        self.mColor = color

    def setRevolutionsPerSecond(self, revolution_per_second):
        self.mRevolutionsPerSecond = revolution_per_second
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self.mTrailFadePercentage = trail

    def setMinimumTrailOpacity(self, min_trail_opacity):
        self.mMinimumTrailOpacity = min_trail_opacity

# End of File
