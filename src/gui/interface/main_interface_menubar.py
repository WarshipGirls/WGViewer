import os
import webbrowser

from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtWidgets import QMenuBar, QAction, QMessageBox

from src import data as wgr_data


class MainInterfaceMenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.qsettings = QSettings(wgr_data.get_qsettings_file(), QSettings.IniFormat)

        self.init_file_menu()
        self.init_view_menu()
        self.init_preferences_menu()
        self.init_help_menu()

    def create_action(self, text, handler, shortcut=None):
        q = QAction(text, self)
        q.triggered.connect(handler)
        if shortcut != None:
            q.setShortcut(shortcut)
        else:
            pass
        return q

    def init_file_menu(self):
        # The ampersand in the menu item's text sets Alt+F as a shortcut for this menu.
        menu = self.addMenu(self.tr("&File"))
        menu.addAction(self.create_action("Open &Cache Folder", self.open_cache_folder))
        menu.addAction(self.create_action("Clear All Cache (CAREFUL!)", self.clear_cache_folder))
        menu.addSeparator()
        menu.addAction(self.create_action("Quit", self.quit_application))

    def init_view_menu(self):
        menu = self.addMenu(self.tr("&View"))
        menu.addAction(self.create_action("&Open Navy Base Overview", self.parent.init_side_dock, "Ctrl+O"))

    def init_preferences_menu(self):
        menu = self.addMenu(self.tr("&Preferences"))
        scheme = menu.addMenu("Color Scheme")
        scheme.addAction(self.create_action("Dark", self.use_qdarkstyle))
        scheme.addAction(self.create_action("Native Bright", self.use_native_style))

    def init_help_menu(self):
        menu = self.addMenu(self.tr("&Help"))
        menu.addAction(self.create_action("&Report a bug", self.submit_issue))
        menu.addSeparator()
        menu.addAction(self.create_action("&About Warship Girls Viewer", self.open_author_info))

    # ================================
    # File QActions
    # ================================

    def quit_application(self):
        # TODO: in the future, save unfinished tasks
        QCoreApplication.exit()

    def open_cache_folder(self):
        os.startfile(wgr_data.get_data_dir())

    def clear_cache_folder(self):
        reply = QMessageBox.question(self, 'Warning', "Do you want to clear all caches?\n(Re-caching takes time)",
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            wgr_data.clear_cache_folder()
        else:
            pass

    # ================================
    # Preferences QActions
    # ================================

    def use_native_style(self):
        self.qsettings.setValue("style", "native")
        self.parent.set_color_scheme()

    def use_qdarkstyle(self):
        self.qsettings.setValue("style", "qdarkstyle")
        self.parent.set_color_scheme()

    # ================================
    # Help QActions
    # ================================

    def submit_issue(self):
        reply = QMessageBox.question(self, 'Report', "Do you want to submit a bug or make an suggestion?",
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            webbrowser.open_new('https://github.com/WarshipGirls/WGViewer/issues/new')
        else:
            pass

    def open_author_info(self):
        def get_hyperlink(link, text):
            return "<a style=\"color:hotpink;text-align: center;\" href='" + link + "'>" + text + "</a>"

        msg_str = '<h1>Warship Girls Viewer</h1>'
        msg_str += "\n"
        msg_str += get_hyperlink('https://github.com/WarshipGirls/WGViewer', 'GitHub - WGViewer')
        QMessageBox.about(self, "About", msg_str)

# End of File
