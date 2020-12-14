from PyQt5.QtCore import QPoint, QRect, QSettings, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QStyle, QStyleOptionTab, QStylePainter,
    QTabBar, QTabWidget,
    QProxyStyle, QMainWindow, QWidget, QStatusBar, QPushButton, QVBoxLayout
)

from src.data.wgv_qsettings import get_qsettings_file
from src.utils.wgv_pyqt import get_user_resolution
from src.data.wgv_qsettings import get_color_scheme
from .setting_tabs import UISettings, GameSettings


class TabBar(QTabBar):
    def __init__(self):
        super().__init__()
        user_w, _ = get_user_resolution()
        self.offset = QSize(int(0.01 * user_w), int(0.01 * user_w))

    def tabSizeHint(self, index):
        # Here defines the rendering size of tab-laber
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        s += self.offset
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())     # place the label text in label
            opt.rect = r

            c = self.tabRect(i).center()
            # rotate the text orientation
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)

            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.qsettings = QSettings(get_qsettings_file(), QSettings.IniFormat)
        self.setTabBar(TabBar())
        self.setTabPosition(QTabWidget.West)
        # self.setStyleSheet(get_color_scheme())
        # can also add QIcon as 2nd argument
        self.ui_settings = UISettings(self.qsettings)
        self.addTab(self.ui_settings, "UI")
        self.game_settings = GameSettings(self.qsettings)
        self.addTab(self.game_settings, "GAME")



''' This seems useless
class ProxyStyle(QProxyStyle):
    def __init__(self):
        super().__init__()

    def drawControl(self, element, opt, painter, widget):
        # This seems useless
        if element == QStyle.CE_TabBarTabLabel:
            r = QRect(opt.rect)
            w = 0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QProxyStyle.drawControl(self, element, opt, painter, widget)
'''


class GlobalSettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setStyle(ProxyStyle())

        # self.layout = QVBoxLayout()
        self.vertical_tabs = TabWidget()

        self.status_bar = QStatusBar()
        self.reset_button = QPushButton('Reset')
        # self.setStatusBar(self.status_bar)
        self.init_ui()
        # self.vertical_tabs.show()
        self.show()

    def init_ui(self) -> None:
        # self.layout.addWidget(self.vertical_tabs)

        # can also add QIcon as 2nd argument
        # self.vertical_tabs.addTab(UISettings(self.qsettings), "UI")
        # self.vertical_tabs.addTab(GameSettings(self.qsettings), "GAME")
        self.setStyleSheet(get_color_scheme())

        user_w, user_h = get_user_resolution()
        w = int(user_w / 3)
        h = int(user_h * 4 / 9)
        # self.vertical_tabs.resize(w, h)
        self.resize(w, h)
        self.setCentralWidget(self.vertical_tabs)
        # can also add QIcon as 2nd argument
        # self.vertical_tabs.addTab(UISettings(self.qsettings), "UI")
        # self.vertical_tabs.addTab(GameSettings(self.qsettings), "GAME")

        self.reset_button.clicked.connect(self.on_reset)
        self.status_bar.addWidget(self.reset_button)
        self.setStatusBar(self.status_bar)
        # self.setLayout(self.layout)
        self.setLayout(QVBoxLayout())

    def on_reset(self) -> None:
        if self.vertical_tabs.currentIndex() == 0:
            self.vertical_tabs.ui_settings.on_reset()
        elif self.vertical_tabs.currentIndex() == 1:
            self.vertical_tabs.game_settings.on_reset()
        else:
            pass

# End of File
