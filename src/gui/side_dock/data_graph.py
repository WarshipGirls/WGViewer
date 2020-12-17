import csv
import os

import plotly.graph_objects as go
import plotly.io as pio

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from src.data import get_user_dir, get_color_scheme, get_color_option
from src.utils import ts_to_date, get_user_resolution
from .constants import CSV_HEADER


class UserDataGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QWebEngineView(self)
        self.resource_data = [[]] * len(CSV_HEADER)

        self.init_ui()

    def init_ui(self) -> None:
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.browser)
        user_w, user_h = get_user_resolution()
        w = int(user_w * 0.52)
        h = int(user_h * 0.74)
        self.resize(w, h)
        self.setLayout(vertical_layout)

    def show_data_graph(self) -> None:
        self.show_graph(1, 5, 'Resources')

    def show_item_graph(self) -> None:
        self.show_graph(6, 11, 'Items')

    def show_core_graph(self) -> None:
        self.show_graph(11, 16, 'Ship Cores')

    def _clean_data(self) -> None:
        self.resource_data = [[]] * len(CSV_HEADER)

    def read_csv(self) -> None:
        csv_file = os.path.join(get_user_dir(), 'resource_log.csv')
        with open(csv_file, 'r') as f:
            csv_input = csv.reader(f)
            next(csv_input)  # skip header
            self._clean_data()
            self.resource_data = list(zip(*[map(int, row) for row in csv_input]))
            self.resource_data[0] = list(map(ts_to_date, self.resource_data[0]))

    def show_graph(self, start_idx: int, end_idx: int, title: str) -> None:
        self.read_csv()
        fig = go.Figure()
        for i in range(start_idx, end_idx):
            fig.add_trace(go.Scatter(
                x=self.resource_data[0],
                y=self.resource_data[i],
                name=CSV_HEADER[i]
            ))
        fig.update_layout(title=title)
        if get_color_option() == "qdarkstyle":
            # TODO? remove the "wide" white margins
            self.setStyleSheet(get_color_scheme())
            fig.layout.template = pio.templates["plotly_dark"]
        else:
            pass
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        self.show()

# End of File
