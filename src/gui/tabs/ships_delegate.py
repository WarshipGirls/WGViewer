from PyQt5.QtWidgets import QStyledItemDelegate


class ShipTableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # Make only column 1 editable
        if index.column() == 1:
            return super(ShipTableDelegate, self).createEditor(parent, option, index)
        else:
            print("clicked " + str(index.column()))


# End of File