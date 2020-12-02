from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction

from src.utils import _quit_application


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent, icon_path):
        super().__init__(parent)
        # All members need to be self referenced (including QAction;
        # otherwise will be collected

        # TODO? in Windows, after restore from tray, the app shows on Windows Taskbar, but not on Desktop
        self.setIcon(QIcon(icon_path))
        self.setVisible(True)
        self.setToolTip('WGViewer')

        self.option_display = QAction()
        if self.parent().isVisible():
            self.option_display.setText('Hide')
        else:
            self.option_display.setText('Display')
        self.option_display.triggered.connect(self.toggle_display)

        self.option_quit = QAction('Quit')
        self.option_quit.triggered.connect(_quit_application)

        self.menu = QMenu()
        self.menu.addAction(self.option_display)
        self.menu.addAction(self.option_quit)
        self.setContextMenu(self.menu)

        self.activated.connect(self.activate_handler)

    def activate_handler(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_display()
        else:
            pass

    def toggle_display(self) -> None:
        if self.parent().isVisible():
            self.option_display.setText('Display')
            self.parent().hide()
        else:
            self.option_display.setText('Hide')
            self.parent().show()

# End of File
