import sys
import os
from customer import CustomerWindow
from PyQt5.QtWidgets import *
from PyQt5 import uic
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

UI_Lot = uic.loadUiType("dialog_customer.ui")[0]
db = firestore.client()