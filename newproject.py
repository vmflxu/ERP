from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from datetime import datetime

from firebase_admin import db, firestore

UI_newproject = uic.loadUiType("dialog_newproject.ui")[0]
db= firestore.client()

class NewProject(QDialog,UI_newproject):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.button_register.clicked.connect(self.register)
        self.button_close.clicked.connect(self.closeDialog)

    def initUI(self):
        self.setupUi(self)
        self.setCombobox()

    def setCombobox(self):
        docs = db.collection("CUSTOMERS").stream()
        combolist = []
        for doc in docs:
            combolist.append(str(doc.id))
        self.comboCustomers.addItems(combolist)

    def register(self):
        customer = self.comboCustomers.currentText()
        project = self.lineEdit.text()
        key = str(datetime.now())
        db.collection("PROJECTS").document(customer).set({key:project},merge=True)
        self.label_report.setText("등록이 완료되었습니다.")
        self.button_register.setDisabled(True)
    
    def closeDialog(self):
        self.close()
        

    # #   등록버튼 이벤트처리
    # def registerPJT(self):
