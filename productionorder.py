from upload import UploadDialog
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont,QFontDatabase
from firebase_admin import firestore
from datetime import datetime


UI_po = uic.loadUiType("ui_po.ui")[0]
UI_calendar = uic.loadUiType("ui_calendar.ui")[0]
UI_works = uic.loadUiType("ui_worklist.ui")[0]
# UI_upload = uic.loadUiType("ui_upload_po.ui")[0]

db = firestore.client()


class PoFrame(QtWidgets.QFrame,UI_po):
    
    # List 선언
    # 항목별 DB Data 저장소 (Item, 공정, 규격) 초기화
    list_item = [""]
    list_work = [""]
    list_spec = [""]
    
    # ComboBox List (Item, 공정, 규격) 초기화
    combo_item = []
    combo_work = []
    combo_spec = []

    end_date = None
     
    def __init__(self):
        super().__init__()
        self.initUI()

        # Calendar Button Click Event Slot
        self.bt_Cal.clicked.connect(self.calButtonClicked)


    def initUI(self):
        self.setupUi(self)
        header = self.tableItem.horizontalHeader()
        
        self.label_important.setStyleSheet("padding-bottom:5px;")
        self.label_worklist.setStyleSheet("padding-bottom:5px;")

        
        # Table Header Width setting
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Interactive)        # Stretch
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(2,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(4,QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(5,QtWidgets.QHeaderView.ResizeToContents)

        self.init_ComboList()
        self.init_Customer()
        self.setItemList()
        self.slotIterator()
        self.slotLabels()
        self.slotUpload()
      
    def init_Customer(self):
        list_customer=["","기타"]
        docs = db.collection('CUSTOMERS').stream()
        for doc in docs:
            list_customer.append(doc.id)
        self.comboCustomer.addItems(list_customer)
    

    def slotLabels(self):
        self.comboCustomer.currentTextChanged.connect(lambda text:self.init_Project(text))
        self.comboCustomer.currentTextChanged.connect(lambda text:self.changeLabelCustomer(text))
        self.comboProject.currentTextChanged.connect(lambda text:self.changeLabelProject(text))
    
    def slotUpload(self):
        self.button_upload.clicked.connect(self.uploadButtonClicked)

    def changeLabelCustomer(self,text):
        self.label_Customer.setText(text)
    def changeLabelProject(self,text):
        self.label_Project.setText(text)

    def init_Project(self,text):
        list_project=[]
        self.comboProject.clear()
        docs = db.collection('PROJECTS').stream()
        for doc in docs:
            if(doc.id == text) :
                temp = doc.to_dict()
                for key in temp :
                    list_project.append(temp[key])
                break
            else:
                continue
        if list_project == []:
           list_project.append("No Project")
        self.comboProject.addItems(list_project)
          
    #   ComboBox Slot Iterator
    def slotIterator(self):
        for i in range(8) :
            self.combo_item[i].currentTextChanged.connect(lambda text, x=i:self.setWorkList(text,x))
            self.combo_work[i].currentTextChanged.connect(lambda text, y=i:self.setSpecList(text,y))

    def slotlength(self):
        for i in range(8):
            self.combo_spec[i].activated.connect(lambda i =i :self.setlength(i))

    #   Combo initiating
    def init_ComboList(self):
        for i in range(0,8,1):
            temp_array = [""]
            temp_item = QComboBox()
            temp_work = QComboBox()
            temp_spec = QComboBox()
            
            
            temp_item.addItems(temp_array)
            temp_work.addItems(temp_array)
            temp_spec.addItems(temp_array)

            self.combo_item.append(temp_item)
            self.combo_work.append(temp_work)
            self.combo_spec.append(temp_spec)
   
            cellindex_work = self.tableItem.model().index(i,0)
            self.tableItem.setIndexWidget(cellindex_work,self.combo_item[i])
            cellindex_work = self.tableItem.model().index(i,1)
            self.tableItem.setIndexWidget(cellindex_work,self.combo_work[i])
            cellindex_spec = self.tableItem.model().index(i,2)            
            self.tableItem.setIndexWidget(cellindex_spec,self.combo_spec[i])

    #   DB로부터 ITEM Collection의 document id를 전부 땡겨와서 List에 Allocating
    def setItemList(self):
        docs = db.collection('ITEM').stream()
        for doc in docs:
            self.list_item.append(doc.id)
    
        for i in range(8):
            self.combo_item[i].clear()
            self.combo_item[i].addItems(self.list_item)
        
    #   item combo 클릭에 대한 event 처리
    def setWorkList(self,text,row):
        self.list_work.clear()
        self.list_work.append("")

        if text !="":
            docs = db.collection(text).stream()
            for doc in docs:
                self.list_work.append(doc.id)
        else :
            self.list_work.clear()
            self.list_work.append("")

        self.combo_work[row].clear()
        self.combo_work[row].addItems(self.list_work)

    #   Work combo 변화 대한 event 처리
    def setSpecList(self,text,row):
        self.list_spec.clear()
        self.list_spec.append("")
        
        if text != "":
            docs = db.collection(self.combo_item[row].currentText()).document(text).get()
            for key,value in docs.to_dict().items():
                self.list_spec.append(value)
        else :
            self.list_spec.clear()
            self.list_spec.append("")

        self.combo_spec[row].clear()
        self.combo_spec[row].addItems(self.list_spec)       

    #   달력 클릭 시 데이터 반환 및 라벨 Text 세팅 구문
    def calButtonClicked(self):
        self.caldialog = Calendar()
        self.caldialog.command.connect(self.setDateLabel)
        self.caldialog.exec_()
    def setDateLabel(self,msg,msg2):
        self.labelDate.setText(msg)
        self.end_date = msg2.toPyDate().strftime("%Y%m%d_%H%M%S")
    
    #   Upload 관련 함수
    def uploadButtonClicked(self):
        self.temp_data = self.setDataset()
        self.upload = UploadDialog()
        self.upload.dataset = self.temp_data
        self.upload.exec_()

    #   Initialization the Dataset and return it
    def setDataset(self):
        self.orderclass = None
        self.dataset={}

        #   have to code exception : no select
        if self.radioPJT.isChecked() :
            self.orderclass = True
        elif self.radioETC.isChecked() :
            self.orderclass = False
        self.now = QDate.currentDate().toPyDate().strftime("%Y%m%d_%H%M%S")
        self.ordernumber = self.getOrderNumber(self.orderclass)
        # self.worklist = self.setDictionary()
        self.customer = str(self.comboCustomer.currentText())
        self.pjt = str(self.comboProject.currentText())
        self.special = str(self.editNote.toPlainText())
        self.dict = self.setDictionary()
        self.dataset = {
            "NUMBER": self.ordernumber,
            "CUSTOMER": self.customer,
            "PJT": self.pjt,
            "ORDERER":"이창익",
            "END_DAY": self.end_date,
            "START_DAY": self.now,
            "SPECIALPOINT": self.special,
            "WORKLIST" : self.dict,
            "STATUS" : "RELEASE"
            }
        return self.dataset

    #   Query and request recent PO Number based on classfication
    #   organized 100000s and 200000s based on classfication
    #   exception for otherwise is ignored.(maybe the company works can't reach that number)
    def getOrderNumber(self,order_class):     
        self.DBlistener = db.collection("PO_PJT")
        self.return_value = 0
        
        if order_class :
            self.query = self.DBlistener.where("NUMBER",'<',200000).order_by("NUMBER",direction=firestore.Query.DESCENDING).limit(1)
        else :
            self.query = self.DBlistener.where("NUMBER",'>=',200000).where("NUMBER",'<',300000).order_by("NUMBER",direction=firestore.Query.DESCENDING).limit(1)
            
        self.results = self.query.stream()
        for doc in self.results:
            self.ponumber = int(doc.to_dict()["NUMBER"])

        self.return_value = int(self.ponumber) + 1
        print(self.return_value)
        
            
        return self.return_value
    
    #   Set User Input and Return it as dictionary
    def setDictionary(self):
        input_dict = {}
        temp = [[None for col in range(6)] for row in range(8)]
        for i in range(8):
            temp[i][0]=str(self.combo_item[i].currentText())
            temp[i][1]=str(self.combo_work[i].currentText())
            temp[i][2]=str(self.combo_spec[i].currentText())
            temp[i][3]=self.IsNoneItemCell(1,i,3)   
            temp[i][4]=self.IsNoneItemCell(1,i,4)   
            temp[i][5]=self.IsNoneItemCell(0,i,5)
            input_dict[i] = temp[i]
        return input_dict

    def IsNoneItemCell(self,boolNum,row,column):
        if boolNum :
            if self.tableItem.item(row,column) == None or self.tableItem.item(row,column).text() == "''" :
                return 0
            elif self.tableItem.item(row,column).text() == '':
                return 0
            else :
                return int(self.tableItem.item(row,column).text())
        else :
            if self.tableItem.item(row,column) == None:
                return ""
            else :
                return str(self.tableItem.item(row,column).text())

#   달력 class : Dialog 띄운 후 달력 선택 --> 선택한 날짜 반환
class Calendar(QDialog,UI_calendar):
    command = QtCore.pyqtSignal(str,QDate)
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.calWidget.clicked[QDate].connect(self.sendDate)
        self.calWidget.activated[QDate].connect(self.sendDate)

    def initUI(self):
        self.setupUi(self)

    def sendDate(self):
        msg = self.calWidget.selectedDate().toString('yyyy.MM.dd (ddd)')
        msg2 = self.calWidget.selectedDate()
        self.command.emit(msg,msg2)
        self.close()
