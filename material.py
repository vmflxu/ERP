from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from firebase_admin import firestore
from status import Status

UI_material = uic.loadUiType("ui_material.ui")[0]

db = firestore.client()

class Material(QtWidgets.QFrame,UI_material):
    itemlist = []
    itemunit = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.signals()
    
    def signals(self):
        self.button_search.clicked.connect(self.slotSearch)
        self.listWidget.itemClicked.connect(self.slotListWidget)
        self.button_cleanroom.clicked.connect(lambda:self.setStatus(self.button_cleanroom.text()))
        self.button_m1.clicked.connect(lambda:self.setStatus(self.button_m1.text()))
        self.button_m2.clicked.connect(lambda:self.setStatus(self.button_m2.text()))
        self.button_stack.clicked.connect(lambda:self.setStatus(self.button_stack.text()))
        self.button_vacuum.clicked.connect(lambda:self.setStatus(self.button_vacuum.text()))
        self.button_yard.clicked.connect(lambda:self.setStatus(self.button_yard.text()))
        self.button_warehouse.clicked.connect(lambda:self.setStatus(self.button_warehouse.text()))
        self.button_B104.clicked.connect(lambda:self.setStatus(self.button_B104.text()))
        self.button_B105.clicked.connect(lambda:self.setStatus(self.button_B105.text()))

    def slotSearch(self):
        self.itemlist.clear()
        self.itemunit = None
        userinput = str(self.lineEdit.text())

        docs = db.collection("MATERIALS").stream()
        for doc in docs :
            if userinput in doc.to_dict().get("ITEM"):
                self.itemlist.append(doc.to_dict().get("ITEM"))
                self.itemunit = doc.to_dict().get("UNIT")
            else:
                continue

        self.setListWidget()

    def setStatus(self,id):
        dialog = Status(id)
        dialog.exec()


    def setListWidget(self):
        self.listWidget.clear()
        for item in self.itemlist:
            self.listWidget.addItem(item)

    def slotListWidget(self,item):
        data = {}
        docs = db.collection("WAREHOUSE").stream()
        for doc in docs:
            data[str(doc.id)] = doc.to_dict().get(item.text())
        self.setLabels(data)
        
    def setLabels(self,data:dict):
        total_headquarter, total_outside, total = 0,0,0
        
        headquarter = [
            self.label_cleanroom
            ,self.label_m1
            ,self.label_m2
            ,self.label_stack
            ,self.label_vacuum
            ,self.label_yard
            ,self.label_warehouse
            ]
        data_headquarter = [
            data["cleanroom"]
            , data["m1"]
            , data["m2"]
            , data["stack"]
            , data["vacuum"]
            , data["yard"]
            , data["warehouse"]
        ]
        map_headquarter = [
            self.label_num_cleanroom
            ,self.label_num_m1
            ,self.label_num_m2
            ,self.label_num_stack
            ,self.label_num_vacuum
            ,self.label_num_yard
            ,self.label_num_warehouse
            ]

        outside = [
            self.label_B104
            ,self.label_B105
            ]
        data_outside = [
            data["B104"]
            ,data["B105"]
            ]
        map_outside = [
            self.label_num_B104
            ,self.label_num_B105
            ]
            
        unitlabels = [
            self.label_unit_0,
            self.label_unit_1,
            self.label_unit_2,
            self.label_unit_3,
            self.label_unit_4,
            self.label_unit_5,
            self.label_unit_6,
            self.label_unit_7,
            self.label_unit_8,
            self.label_unit_9,
            self.label_unit_10,
            self.label_unit_11
            ]
        
        for item_HQ in data_headquarter:
            total_headquarter = total_headquarter + item_HQ

        for item_outside in data_outside:
            total_outside = total_outside + item_outside

        for i in range(len(headquarter)):
            headquarter[i].setText(str(data_headquarter[i]))
            map_headquarter[i].setText(str(data_headquarter[i]))

        for j in range(len(outside)):
            outside[j].setText(str(data_outside[j]))
            map_outside[j].setText(str(data_outside[j]))

        for label in unitlabels:
            label.setText(self.itemunit)
            label.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.label_HQ_total.setText(str(total_headquarter))
        self.label_MF_total.setText(str(total_outside))
        
        total = total_headquarter + total_outside
        self.label_total.setText(str(total))
