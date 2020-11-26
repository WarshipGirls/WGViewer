from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate

from .equip_window import EquipPopup


class ShipTableDelegate(QStyledItemDelegate):
    def __init__(self, view):
        super().__init__()
        self._view = view

    def createEditor(self, parent, option, index):
        if index.column() == 1:
            # Make only column 1 editable
            return super(ShipTableDelegate, self).createEditor(parent, option, index)
        elif 21 <= index.column() <= 24: 
            # TODO? THIS is probably NOT the way it should be done. but I don't know how to do it otherwise
            print("clicked equip " + str(index.row()) + ", " + str(index.column()))
            cid = index.sibling(index.row(), 0).data(Qt.UserRole)
            btn_on = True if int(index.data(Qt.UserRole)) > 0 else False
            self._equip_popup(index.row(), index.column(), cid, btn_on)
        else:
            print("clicked " + str(index.row()) + ", " + str(index.column()))

    def _equip_popup(self, row, col, cid, btn_on):
        self.w = EquipPopup(self, row, col, cid, btn_on)
        self.w.show()

    def handle_event(self, row, col, eid):
        # the chain of following is disgusting
        self._view.model().sourceModel().update_one_equip(row, col, str(eid))
        self.w.close()


# End of File