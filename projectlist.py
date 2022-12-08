from newproject import NewProject
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtCore import Qt

from firebase_admin import db, firestore


UI_projectlist = uic.loadUiType("ui_projectlist.ui")[0]
db = firestore.client()

class ProjectList(QtWidgets.QFrame,UI_projectlist):
    dataset=[]

    def __init__(self):
        super().__init__()
        self.initUI()
        self.button_register.clicked.connect(self.registerNew)
        self.button_refresh.clicked.connect(self.refreshTable)
        # self.button_modify.clicked.connect(self.modifyPJT)

    def initUI(self):
        self.setupUi(self)
        self.setProjectList()
        self.getTableModel()

    #   refresh
    def refreshTable(self):
        self.dataset = []
        self.setProjectList()
        self.getTableModel()

    #   read DB and return it as 2 dimensional List
    def setProjectList(self):        
        docs = db.collection("PROJECTS").stream()
        for doc in docs:
            for value in doc.to_dict().values():
                temp =[]
                temp.append(str(doc.id))
                temp.append(value)
                self.dataset.append(temp)
        
    #   get TableModel using dataset
    def getTableModel(self):
        print(type(self.dataset))
        self.model = TableModel(self.dataset)
        self.model.setHeaderData(0, Qt.Horizontal, "업체명")
        self.model.setHeaderData(1, Qt.Horizontal, "프로젝트")
        self.tablePJT.setModel(self.model)

    #   등록버튼 이벤트 처리
    def registerNew(self):
        self.register = NewProject()
        self.register.exec()
        


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
        headerlist = ["업체명","프로젝트"]
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return headerlist[section]
        return super().headerData(section, orientation, role)