from PyQt5.QtCore import QThread

class Worker(QThread):
    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        print("ideal amounts of thread to run on current OS: " + str(QThread.idealThreadCount()))

    def run(self):
        self.func(*self.args)

# End of File