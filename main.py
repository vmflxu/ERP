# 메인윈도우
import sys

# import ERP Modules
from customer import CustomerWindow
from productionorder import PoFrame
from projectlist import ProjectList
from mainframe import MainFrame
from polist import PoList
from material import Material

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Connect Firebase: json file, below, has the information set for connecting DB
credential_path = "tsc-erp-firebase-adminsdk-apb5k-f725d83303.json"

cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred,None,'main')

db = firestore.client()

# Qtdesigner로 작성한 ui파일 연동
UI_class = uic.loadUiType("untitled.ui")[0]


class MainWindow(QMainWindow,QAction,QtWidgets.QFrame,UI_class):
    def __init__(self):
        if __name__ == '__main__':
            super().__init__()
            self.initUI()

    # layout 구성 및 메뉴 선택시 Action
    def initUI(self):
        # Ui 파일 셋업 (이하 모든 코드의 ui 셋업은 동일하게 진행함)
        self.setupUi(self)

        self.set_Framestack()
        self.action_Customer.triggered.connect(self.menu_Customer)
        self.action_Newpo.triggered.connect(self.menu_Po)
        self.action_Project.triggered.connect(self.menu_ProjectList)
        self.action_Polist.triggered.connect(self.menu_PoList)
        self.action_Material.triggered.connect(self.menu_Material)

    # 거래처 선택시 팝업
    def menu_Customer(self):
        self.second = CustomerWindow()
        self.second.exec_()

    # MainFrame Stack 세팅 : 새로운 ERP 모듈 추가 시 QFrame으로 화면을 구성할 경우, 이곳에 추가 작업 진행할 것.
    def set_Framestack(self):
        self.frame_main = MainFrame()
        self.frame_po = PoFrame()
        self.frame_projectlist = ProjectList()
        self.frame_polist = PoList()
        self.frame_material = Material()
        self.mainStackedWidget.addWidget(self.frame_main)
        self.mainStackedWidget.addWidget(self.frame_po)
        self.mainStackedWidget.addWidget(self.frame_projectlist)
        self.mainStackedWidget.addWidget(self.frame_polist)
        self.mainStackedWidget.addWidget(self.frame_material)

        self.mainStackedWidget.setCurrentIndex(1)         # 기본 mainframe

    def menu_Po(self):
        self.mainStackedWidget.setCurrentIndex(2)
    def menu_ProjectList(self):
        self.mainStackedWidget.setCurrentIndex(3)
    def menu_PoList(self):
        self.mainStackedWidget.setCurrentIndex(4)
    def menu_Material(self):
        self.mainStackedWidget.setCurrentIndex(5)

app = QApplication(sys.argv)

window = MainWindow()

window.showMaximized()

sys.exit(app.exec_())
