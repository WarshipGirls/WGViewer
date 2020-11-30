from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):
    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        # TODO assign task based on user thread power
        print("ideal amounts of thread to run on current machine: " + str(QThread.idealThreadCount()))

    def run(self):
        self.func(*self.args)


class LoginWorker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, _func, args, callback):
        super().__init__()
        self._func = _func
        self.args = args
        self.finished.connect(callback)

    def run(self):
        res = self._func(*self.args)
        res = True if res is True else False
        self.finished.emit(res)

# End of File
