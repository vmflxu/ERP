from PyQt5 import uic, QtWidgets

UI_mainframe = uic.loadUiType("ui_mainframe.ui")[0]

class MainFrame(QtWidgets.QFrame,UI_mainframe):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
