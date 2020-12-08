import os
import sys
from typing import Callable
from urllib.request import urlopen

from PyQt5.QtCore import QSettings, pyqtSlot
from PyQt5.QtWidgets import QMenuBar, QAction, QMessageBox

from src import data as wgv_data
from src import utils as wgv_utils
from src.gui.custom_widgets import ScrollBoxWindow


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class MainInterfaceMenuBar(QMenuBar):
    # TODO if I want to denote the parent type as MainInterface; how to avoid recursive import?
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.qsettings = QSettings(wgv_data.get_qsettings_file(), QSettings.IniFormat)
        self.version_log = None

        self.init_file_menu()
        self.init_tabs_menu()
        self.init_view_menu()
        self.init_links_menu()
        self.init_preferences_menu()
        # self.init_developers_menu()
        self.init_help_menu()

    def create_action(self, text: str, handler: Callable, shortcut=None) -> QAction:
        q = QAction(text, self)
        q.triggered.connect(handler)
        if shortcut is not None:
            q.setShortcut(shortcut)
        else:
            pass
        return q

    def init_file_menu(self) -> None:
        # The ampersand in the menu item's text sets Alt+F as a shortcut for this menu.
        menu = self.addMenu(self.tr("&File"))
        menu.addAction(self.create_action("Open &Cache Folder", self.open_cache_folder))
        menu.addAction(self.create_action("Clear User Cache", self.clear_user_cache))
        menu.addAction(self.create_action("Clear All Cache", self.clear_all_cache))
        menu.addSeparator()
        menu.addAction(self.create_action("Quit", wgv_utils.quit_application))

    def init_tabs_menu(self) -> None:
        menu = self.addMenu(self.tr("&Tabs"))
        menu.addAction(self.create_action("Open &Advance Tab", lambda: self.parent.main_tabs.add_tab('tab_adv'), "Ctrl+A"))
        menu.addAction(self.create_action("Open &Dock Tab", lambda: self.parent.main_tabs.add_tab('tab_dock'), "Ctrl+D"))
        menu.addAction(self.create_action("Open &Expedition Tab", lambda: self.parent.main_tabs.add_tab('tab_exp'), "Ctrl+E"))
        menu.addAction(self.create_action("Open &Thermopylae Tab", lambda: self.parent.main_tabs.add_tab('tab_thermopylae'), "Ctrl+T"))

    def init_view_menu(self) -> None:
        menu = self.addMenu(self.tr("&View"))
        menu.addAction(self.create_action("Open &Navy Base Overview", self.parent.create_side_dock, "Ctrl+N"))

    def init_preferences_menu(self) -> None:
        menu = self.addMenu(self.tr("&Preferences"))
        # sub menu
        scheme = menu.addMenu("Color Scheme")
        scheme.addAction(self.create_action("Dark", self.use_qdarkstyle))
        scheme.addAction(self.create_action("Native Bright", self.use_native_style))

    def init_links_menu(self) -> None:
        menu = self.addMenu(self.tr("&Links"))
        menu.addAction(self.create_action("Show Game App Download Links", self.show_download_links))

    # def init_developers_menu(self) -> None:
    # menu = self.addMenu(self.tr("&Developers"))

    def init_help_menu(self) -> None:
        menu = self.addMenu(self.tr("&Help"))
        menu.addAction(self.create_action("&Bug Report / Feature Request", self.submit_issue))
        menu.addSeparator()
        menu.addAction(self.create_action("WGViewer &Version Logs", self.open_version_log))
        menu.addAction(self.create_action("&About Warship Girls Viewer", self.open_author_info))

    # ================================
    # File QActions
    # ================================

    @staticmethod
    def quit_application() -> None:
        wgv_utils.quit_application()

    @staticmethod
    def open_cache_folder() -> None:
        os.startfile(wgv_data.get_data_dir())

    @staticmethod
    def clear_user_cache() -> None:
        res = wgv_data.clear_cache_folder(False)
        if res is True:
            wgv_utils.popup_msg('Clear success')
        else:
            wgv_utils.popup_msg('Clear failed')

    def clear_all_cache(self) -> None:
        reply = QMessageBox.question(self, 'Warning', "Do you want to clear all caches?\n(Re-caching takes time)",
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            res = wgv_data.clear_cache_folder(True)
            if res is True:
                wgv_utils.popup_msg('Clear success')
            else:
                wgv_utils.popup_msg('Clear failed')
        else:
            pass

    # ================================
    # Links QActions
    # ================================

    @staticmethod
    def show_download_links() -> None:
        def get_hyperlink(link, text) -> str:
            return f"<a href=\"{link}\">{text}</a>"
        version = wgv_utils.get_game_version()
        base_url = "http://bspackage.moefantasy.com/jn/"
        cn_android_full_link = base_url + f"warshipgirlsr_cn_censor_v{version}.apk"
        cn_ios_user_android_full_link = base_url + f"warshipgirlsr_ios_cn_censor_v{version}.apk"

        cn_android_base_link = base_url + f"warshipgirlsr_cn_censor_base_v{version}.apk?"
        cn_ios_user_android_base_link = base_url + f"warshipgirlsr_ios_cn_censor_base_v{version}.apk?"

        msg_str = "<h1> Warship Girls Official Download Links</h1>"
        msg_str += "<br>"
        msg_str += "Click link will auto start downloading in your default browser."
        msg_str += "<br><br>"
        msg_str += get_hyperlink(cn_android_full_link, 'CN Android full package')
        msg_str += "<br>"
        msg_str += get_hyperlink(cn_ios_user_android_full_link, 'CN Android (iOS server) full package')
        msg_str += "<br><br>"
        msg_str += get_hyperlink(cn_android_base_link, 'CN Android base package')
        msg_str += "<br>"
        msg_str += get_hyperlink(cn_ios_user_android_base_link, 'CN Android (iOS server) base package')

        msg = QMessageBox()
        msg.setStyleSheet(wgv_data.get_color_scheme())
        msg.setWindowTitle('Official Game App Download Links')
        msg.setText(msg_str)
        msg.exec_()

    # ================================
    # Preferences QActions
    # ================================

    def use_native_style(self) -> None:
        self.qsettings.setValue("style", "native")
        self.parent.set_color_scheme()

    def use_qdarkstyle(self) -> None:
        self.qsettings.setValue("style", "qdarkstyle")
        self.parent.set_color_scheme()

    # ================================
    # Help QActions
    # ================================

    def submit_issue(self) -> None:
        reply = QMessageBox.question(self, 'Report', "Do you want to submit a bug or make an suggestion?",
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            wgv_utils.open_url('https://github.com/WarshipGirls/WGViewer/issues/new')
        else:
            pass

    def open_version_log(self) -> None:
        text = urlopen('https://raw.githubusercontent.com/WarshipGirls/WGViewer/master/docs/version_log.md').read().decode('ascii')
        self.version_log = ScrollBoxWindow(self, 'WGViewer Version Logs', text)
        self.version_log.setStyleSheet(wgv_data.get_color_scheme())
        self.version_log.show()

    @pyqtSlot()
    def delete_version_log(self) -> None:
        self.version_log.deleteLater()
        self.version_log = None

    @staticmethod
    def open_author_info() -> None:
        def get_hyperlink(link, text) -> str:
            return "<a style=\"color:hotpink;\" href='" + link + "'>" + text + "</a>"

        banner_path = get_data_path('assets/banner.png')
        msg_str = f'<img src=\"{banner_path}\" width=\"400\" height=\"120\">'
        msg_str += '<br><br>'
        msg_str += "> "
        msg_str += get_hyperlink('https://github.com/WarshipGirls/WGViewer', 'WGViewer @ Github')
        msg_str += '<br><br>'
        msg_str += "<p style=\"text-align: center;\">&copy; GNU General Public License v3.0</p>"
        msg = QMessageBox()
        msg.setStyleSheet(wgv_data.get_color_scheme())
        msg.setWindowTitle('About Warship Girls Viewer (WGViewer)')
        msg.setText(msg_str)
        msg.exec_()

# End of File
