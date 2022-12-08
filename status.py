from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from firebase_admin import firestore

UI_Status = uic.loadUiType("dialog_status.ui")[0]

db = firestore.client()

class Status(QDialog, UI_Status):
    id = None
    def __init__(self,input):
        super().__init__()
        self.initUI()
        self.setDataset(input)
        self.button_close.clicked.connect(self.close)

    def initUI(self):
        self.setupUi(self)

    def setDataset(self,input):
        self.id = input
        self.label_title.setText(self.id)