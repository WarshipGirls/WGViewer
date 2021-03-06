import csv

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QStandardItem, QStandardItemModel, QCloseEvent
from PyQt5.QtWidgets import (
    QWidget,
    QHeaderView, QTableView,
    QVBoxLayout
)

from src.utils import get_user_resolution, get_big_success_rate, get_color_scheme


class ExpTable(QWidget):
    sig_close = pyqtSignal()

    # Long term TODO: max coefficient by iter through user's engineering bay stats
    def __init__(self, parent, filename: str):
        super().__init__()
        self.parent = parent
        self.filename = filename

        self.sig_close.connect(self.parent.on_table_close)

        self.table_model = QStandardItemModel(self)
        self.set_col_count(15)
        self.table_view = QTableView(self)
        self.table_view.setModel(self.table_model)
        self.load_csv(self.filename)
        self.set_expectation_income()
        self.set_success_rate()
        self.init_ui()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.table_view)

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.sig_close.emit()

    # ================================
    # Getter / Setter
    # ================================

    def set_col_count(self, cols: int) -> None:
        self.table_model.setColumnCount(cols)

    def get_row_count(self) -> int:
        return self.table_model.rowCount()

    def get_col_count(self) -> int:
        return self.table_model.columnCount()

    # ================================
    # UI
    # ================================

    def init_ui(self) -> None:
        self.setStyleSheet(get_color_scheme())
        self.merge_cells()
        self.init_header_ui()
        self.highlight_data([3, 4, 5, 6], highlight_color=None, bold=True)
        self.highlight_data([7, 8, 9, 10], highlight_color=QColor(128, 159, 255), bold=True)
        self.highlight_data([11, 12, 13, 14], highlight_color=QColor(0, 153, 51), bold=True)

        self.table_view.setShowGrid(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.horizontalHeader().hide()
        self.table_view.verticalHeader().hide()
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        user_w, user_h = get_user_resolution()
        for i in range(self.get_row_count()):
            self.table_view.setRowHeight(i, int(0.019 * user_h))
        _w = int(user_w * 0.443)
        _h = int(user_h * 0.713)
        self.resize(_w, _h)

    def init_header_ui(self) -> None:
        for c in [3, 7, 11]:
            item = self.table_model.itemFromIndex(self.table_model.index(0, c))
            f = item.font()
            f.setBold(True)
            item.setFont(f)
        for c in range(self.get_col_count()):
            item = self.table_model.itemFromIndex(self.table_model.index(1, c))
            item.setBackground(QColor(89, 89, 89))

    def merge_cells(self) -> None:
        self.table_view.setSpan(0, 0, 1, 3)
        self.table_view.setSpan(0, 3, 1, 4)
        self.table_view.setSpan(0, 7, 1, 4)
        self.table_view.setSpan(0, 11, 1, 2)

    def highlight_data(self, cols: list, highlight_color: QColor = None, bold: bool = False) -> None:
        indices = []
        for col in cols:
            indices += self.get_n_max_val_idx_by_col(col)
        maps = set()
        for i in indices:
            item = self.table_model.itemFromIndex(i)
            if isinstance(highlight_color, QColor):
                maps.add(item.row())
                item.setBackground(highlight_color)
                item.setForeground(QColor('black'))
            else:
                pass
            if bold:
                f = item.font()
                f.setBold(True)
                item.setFont(f)
            else:
                pass
        for m in maps:
            item = self.table_model.itemFromIndex(self.table_model.index(m, 0))
            item.setBackground(QColor(0, 153, 51))

    # ================================
    # Data processing
    # ================================

    def load_csv(self, csv_path: str) -> None:
        with open(csv_path, "r") as f:
            for row in csv.reader(f):
                items = [QStandardItem(field) for field in row]
                self.table_model.appendRow(items)

    def set_success_rate(self) -> None:
        raw, n, d = get_big_success_rate()
        item = QStandardItem(str(raw))
        item.setToolTip(f'Expedition Detail\nSuccess\t\t{n}\nGrate Success\t{d}')
        self.table_model.setItem(0, self.get_col_count() - 1, item)

    def set_expectation_income(self) -> None:
        rate, _, _ = get_big_success_rate()
        for row in range(2, self.get_row_count()):
            for col in [11, 12, 13, 14]:
                d = self.table_model.index(row, col - 4).data()
                if d == "":
                    continue
                else:
                    d = int(d)
                    t = (1 - rate) * d + rate * d * 1.5
                    self.table_model.setItem(row, col, QStandardItem(str(int(t))))

    def get_n_max_val_idx_by_col(self, col: int, n: int = 4) -> list:
        tmp = {}
        for row in range(2, self.get_row_count()):
            idx = self.table_model.index(row, col)
            d = idx.data()
            if d == "":
                continue
            else:
                if int(d) in tmp:
                    pass
                else:
                    tmp[int(d)] = []
                tmp[int(d)].append(idx)
        tmp_sorted = sorted(tmp, reverse=True)
        l = count = 0
        r = 1
        res = []
        while r != len(tmp_sorted):
            if tmp_sorted[l] != tmp_sorted[r]:
                count += 1
            else:
                pass
            res += tmp[tmp_sorted[l]]
            l += 1
            r += 1
            if count != n:
                pass
            else:
                break
        return res

# End of File
