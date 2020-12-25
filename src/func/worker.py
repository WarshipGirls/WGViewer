from PyQt5.QtCore import QThread, pyqtSignal


# TODO? assign task based on user thread power

class Worker(QThread):
    """
    bee = Worker(start_func, (iterable args; if single, use [arg]))
    bee.finished.connect(on_finished_func)
    bee.terminate()
    bee.start()
    """
    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        # print("ideal amounts of thread to run on current machine: " + str(QThread.idealThreadCount()))

    def run(self) -> None:
        self.func(*self.args)


class CallbackWorker(QThread):
    """
    bee = CallbackWorker(start_func, (iterable args; if single, use [arg]), on_finished_func)
    bee.terminate()
    bee.start()
    """
    finished = pyqtSignal(object)

    def __init__(self, _func, args, callback):
        super().__init__()
        self._func = _func
        self.args = args
        self.finished.connect(callback)

    def run(self) -> None:
        res = self._func(*self.args)
        self.finished.emit(res)

# End of File
