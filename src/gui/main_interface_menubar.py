import os

from PyQt5.QtWidgets import QMenuBar, QAction, QMessageBox

from ..data import data as wgr_data


class MainInterfaceMenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.init_file_menu()
        self.init_view_menu()
        self.init_preferences_menu()
        self.init_help_menu()

    def init_file_menu(self):
        menu = self.addMenu("File")
        cache_open_action = QAction("Open Cache Folder", self)
        cache_open_action.triggered.connect(self.open_cache_folder)
        menu.addAction(cache_open_action)

        # cache_clear_action = QAction("Clear Cache Folder", self)
        # cache_clear_action.triggered.connect(self.clear_cache_folder)
        # menu.addAction(cache_clear_action)

        menu.addSeparator()

        menu.addAction("Quit")
        # https://stackoverflow.com/q/38283705/14561914

    def init_view_menu(self):
        menu = self.addMenu("View")
        sidedock_action = QAction("&Open Navy Base Overview", self)
        sidedock_action.setShortcut("Ctrl+O")
        # sidedock_action.setStatusTip("...")
        sidedock_action.triggered.connect(self.parent.init_side_dock)
        menu.addAction(sidedock_action)

    def init_preferences_menu(self):
        menu = self.addMenu("Preferences")
        scheme = menu.addMenu("Color Scheme")
        # TODO
        scheme.addAction("Bright (Native)")
        scheme.addAction("Dark")

    def init_help_menu(self):
        menu = self.addMenu("Help")
        about_action = QAction("&About Warship Girls Viewer", self)
        about_action.triggered.connect(self.open_author_info)
        menu.addAction(about_action)


    # ================================
    # QActions
    # ================================


    def open_cache_folder(self):
        path = wgr_data._get_data_dir()
        os.startfile(path)

    # def clear_cache_folder(self):
    #     wgr_data._clear_cache()

    def open_author_info(self):
        def get_hyperlink(link, text):
            return "<a style=\"color:hotpink;text-align: center;\" href='"+link+"'>"+text+"</a>"

        msg_str = '<h1>Warship Girls Viewer</h1>'
        msg_str += "\n"
        msg_str += get_hyperlink('https://github.com/WarshipGirls/WGViewer', 'GitHub - WGViewer')
        QMessageBox.about(self, "About", msg_str)


# End of File