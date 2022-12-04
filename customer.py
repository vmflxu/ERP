import sys

import PyQt5.QtGui

from newcustomer import NewCustomer
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import firebase_admin
from firebase_admin import credentials, db, firestore


UI_customer = uic.loadUiType("dialog_customer.ui")[0]
db = firestore.client()


class CustomerWindow(QDialog,UI_customer):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.buttonNewcustomer.clicked.connect(self.button_newcustomer)

    def initUI(self):
        self.setupUi(self)
        docs = db.collection("CUSTOMERS").stream()
        data = []
        for doc in docs:
            # print(f'{doc.id} => {doc.to_dict()}')
            a = []
            b = doc.to_dict()
            a.append(doc.id)
            a.append(b["FAX"])
            a.append(b["TEL"])
            a.append(b["address"])
            a.append(b["delivery 1"])
            a.append(b["delivery 2"])
            data.append(a)



        self.model = TableModel(data)
        self.model.setHeaderData(0, Qt.Horizontal, "업체명")
        self.model.setHeaderData(1, Qt.Horizontal, "FAX")
        self.model.setHeaderData(2, Qt.Horizontal, "대표전화")
        self.model.setHeaderData(3, Qt.Horizontal, "주소")
        self.model.setHeaderData(4, Qt.Horizontal, "착지1")
        self.model.setHeaderData(5, Qt.Horizontal, "착지2")
        self.tableView.setModel(self.model)

    def button_newcustomer(self):
        self.pushbutton = NewCustomer()
        self.pushbutton.exec()

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
        # See below for the nested-list data structure.
        # .row() indexes into the outer list,
        # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
    # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
    # The following takes the first sub-list, and returns
    # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        headerlist = ["업체명","FAX","대표전화","주소","착지1","착지2"]
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return headerlist[section]
        return super().headerData(section, orientation, role)