from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont,QFontDatabase
from firebase_admin import firestore

UI_material = uic.loadUiType("ui_material.ui")[0]

class Material(QtWidgets.QFrame,UI_material):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)