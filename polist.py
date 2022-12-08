from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIntValidator

from firebase_admin import db, firestore


UI_polist = uic.loadUiType("ui_polist.ui")[0]
UI_calendar = uic.loadUiType("ui_calendar.ui")[0]
db = firestore.client()

class PoList(QtWidgets.QFrame,UI_polist):
    msglist=[]

    def __init__(self):
        super().__init__()
        self.initUI()
        self.slotGroupBoxSearch()
        self.slotButtons()
        self.slotListWidget()

    def initUI(self):
        self.setupUi(self)
        self.setGroupBoxCondition()
        self.setGroupBoxSearch()       


    def setGroupBoxCondition(self):
        self.radio_ordernumber.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio_ordernumber)
        vbox.addWidget(self.radio_orderdate)
        
        self.groupBox_condition.setLayout(vbox)

    def setGroupBoxSearch(self):
        self.hbox_ordernumber = QHBoxLayout()
        self.hbox_ordernumber.addWidget(self.edit_ordernumber)
        #   restrict type of the input data
        self.setInputType()
        self.edit_ordernumber.setReadOnly(False)
        self.button_from.setEnabled(False)
        self.button_to.setEnabled(False)
        self.groupBox_ordernumber.setLayout(self.hbox_ordernumber)

    def slotGroupBoxSearch(self):
        self.radio_ordernumber.toggled.connect(lambda:self.changeGroupBoxByRadio(True))
        self.radio_orderdate.toggled.connect(lambda:self.changeGroupBoxByRadio(False))
    
    def slotButtons(self):
        self.button_from.clicked.connect(lambda:self.calButtonClicked(True))
        self.button_to.clicked.connect(lambda:self.calButtonClicked(False))
        self.button_search.clicked.connect(self.searchDB)

    def slotListWidget(self):
        self.list_order.itemClicked.connect(self.setOrderContents)

    def changeGroupBoxByRadio(self,condition):
        self.edit_ordernumber.setReadOnly(not condition)
        self.button_from.setEnabled(not condition)
        self.button_to.setEnabled(not condition)
        
    def setInputType(self):
        self.typeInt = QIntValidator()
        self.edit_ordernumber.setValidator(self.typeInt)

    def setOrderContents(self,item):
        doc = db.collection("PO_PJT").document(self.match[item.text()]).get()
        startday = str(doc.to_dict()["START_DAY"]).split('_')[0]
        endday = str(doc.to_dict()["END_DAY"]).split('_')[0]\
        
        startday = startday[0:4]+'.'+startday[4:6]+'.'+startday[6:]
        endday = endday[0:4]+'.'+endday[4:6]+'.'+endday[6:]

        self.label_order.setText(str(doc.to_dict()["NUMBER"]))
        self.label_start.setText(startday)
        self.label_end.setText(endday)
        self.label_orderer.setText(str(doc.to_dict()["ORDERER"]))
        self.label_customer.setText(str(doc.to_dict()["CUSTOMER"]))
        self.label_PJT.setText(str(doc.to_dict()["PJT"]))
        self.label_special.setText(str(doc.to_dict()["SPECIALPOINT"]))
        self.setTable(doc.to_dict()["WORKLIST"])

    def setTable(self,dictWorks):
        i = 0
        row = 0
        column = 0
        sortedDict = {}
        while i<8 :
            if dictWorks[str(i)] == None or dictWorks[str(i)] == False :
                break
            else :
                sortedDict[str(i)] = dictWorks[str(i)]
                i = i + 1

        for each_list in sortedDict:
            for data in dictWorks[each_list]:
                if type(data) != str:
                    if data == 0 :
                        self.tableWidget.setItem(row,column,QTableWidgetItem(""))
                    else:
                        self.tableWidget.setItem(row,column,QTableWidgetItem(str(data)))
                else:
                    self.tableWidget.setItem(row,column,QTableWidgetItem(data))
                column = column + 1
            row = row + 1
            column = 0

    #   Calendar 분기 처리
    def calButtonClicked(self,id):
        self.caldialog = Calendar()
        self.caldialog.command.connect(self.saveEmit)
        self.caldialog.exec_()
        self.setDateLabel(self.msglist[0],self.msglist[1],id)
    def saveEmit(self,msg,msg2):
        self.msglist=[]
        self.msglist.append(msg)
        self.msglist.append(msg2)
    def setDateLabel(self,msg,msg2,id):
        if id == True :
            self.label_from.setText(msg)
            self.date_from = msg2.toPyDate().strftime("%Y%m%d_%H%M%S")
        else:
            self.label_to.setText(msg)
            self.date_to = msg2.toPyDate().strftime("%Y%m%d_%H%M%S")

    #   검색버튼 이벤트처리
    def searchDB(self):
        #   다수 실시를 대비하여 초기화
        self.targetOrder = []
        self.list_order.clear()
        #   코드작성이 용이하게 ordernumber와 db 문서id를 연결한 Dictionary
        self.match = {}
        #   self.itemmodel = QStandardItemModel()
        col = db.collection("PO_PJT")        

        #   Radiobutton 분기
        if self.radio_ordernumber.isChecked():
            self.docs = col.where("NUMBER",'==',int(self.edit_ordernumber.text())).stream()
        elif self.radio_orderdate.isChecked():
            self.docs = col.where("START_DAY",'>=',self.date_from).where("START_DAY",'<=',self.date_to).stream()
        
        #   stream() 반환값 없을 시 예외처리 및 listview에 데이터모델 할당
        if self.docs == None:            
            self.targetOrder.append("Nothing")
        else:
            for doc in self.docs:
                self.targetOrder.append(str(doc.to_dict()["NUMBER"]))
                self.match.update({str(doc.to_dict()["NUMBER"]):str(doc.id)})
            self.targetOrder.sort()
            for factor in self.targetOrder:
                self.list_order.addItem(factor)
            
class Calendar(QDialog,UI_calendar):
    command = QtCore.pyqtSignal(str,QDate)
    def __init__(self):
        super().__init__()
        self.initUI()
        self.calWidget.activated[QDate].connect(self.sendDate)

    def initUI(self):
        self.setupUi(self)

    def sendDate(self):
        msg = self.calWidget.selectedDate().toString('yyyy.MM.dd (ddd)')
        msg2 = self.calWidget.selectedDate()
        self.command.emit(msg,msg2)
        self.close()