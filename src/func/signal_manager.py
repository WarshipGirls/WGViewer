from PyQt5.QtCore import QObject, pyqtSignal


class SignalManager(QObject):
    # sig_fuel = pyqtSignal(int)
    raise NotImplementedError


'''
# Example of updating signal cross-thread
# https://stackoverflow.com/a/56617929/14561914
class SignalManager(QtCore.QObject):
    fooSignal = QtCore.pyqtSignal(int, int, QtCore.QVariant)
if __name__ == "__main__":
    def timer(obj):
        idc = 1001
        while True:
            obj.fooSignal.emit(0, 0, idc)
            idc += 1
            time.sleep(1)
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    foo = SignalManager()
    tableView = QtWidgets.QTableView()
    myModel = CopterDataModel()
    foo.fooSignal.connect(myModel.update_item)
    tableView.setModel(myModel)
    tableView.show()
    t = threading.Thread(target=timer, args=(foo,), daemon=True)
    t.start()
    app.exec_()
'''

# End of File
