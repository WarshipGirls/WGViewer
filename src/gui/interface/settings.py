from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QStyle, QStyleOptionTab, QStylePainter,
    QTabBar, QTabWidget,
    QProxyStyle, QMainWindow, QWidget
)

from src.utils.wgv_pyqt import get_user_resolution


class TabBar(QTabBar):
    def __init__(self):
        super().__init__()

    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
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
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabBar(TabBar())
        self.setTabPosition(QTabWidget.West)


class ProxyStyle(QProxyStyle):
    def __init__(self):
        super().__init__()

    def drawControl(self, element, opt, painter, widget):
        if element == QStyle.CE_TabBarTabLabel:
            r = QRect(opt.rect)
            w = 0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QProxyStyle.drawControl(self, element, opt, painter, widget)


class GlobalSettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyle(ProxyStyle())
        self.vertical_tabs = TabWidget()
        self.vertical_tabs.addTab(QWidget(), QIcon("assets/favicon.ico"), "ABC")
        # self.vertical_tabs.addTab(, QIcon("assets/favicon.ico"), "ABC")
        user_w, user_h = get_user_resolution()
        w = int(user_w / 3)
        h = int(user_h * 4 / 9)
        self.vertical_tabs.resize(w, h)
        self.vertical_tabs.show()

# End of File
