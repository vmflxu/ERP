import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
#
# app = QApplication(sys.argv)
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "tsc-erp",
  "private_key_id": "f725d83303ad25600210f73b785ba744912cfb44",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDd0AI22Riciei6\nmriTghBaSgFwf2S+avhHgImIczAVUJjeFDK8cJhSn/N8wd83jf3jhiAyonN4fsE3\ns2tQJtyLfYs3dT6zRIf0fZq/U6w1dLtTfHJTEsbXeCXZf8T6XjlJnJHnLtQh6rCa\nF4Qbp4ztFShBNJlfg58o0fsGGkEqXleKEcR2w2XEr/eHeSh3+ZECbM6AWYW7c6Ki\n3mC2D7foXwy2gwOOWkSKfkxCRTplAId3s9NZb5YhelKLpKwJd7FqxXu+jZGggqAF\nlXVBbi6WrOlVnMz0+Cdizo5jIiur94Nz1yha4m/k8GUvvWaIV23/eXjHZh9NnVcv\n8WO+c7Z5AgMBAAECggEAA3KdljH+/+/k04G0J2wjdO58Nz4ZAsdcNJWljZ68u0LA\nHYjoK6WpuHRkBHxpoSNuiYAm3/fxHjOvgn4iHOIoa21Nd1SLNPN2aYZ08U8Lo4kS\nSv8+3QEIYNutOu7m0OgbW9mN1a9p/LJOgcFRJweOWTZgTyMnfySR72spdl7SGdEg\n2A1rnqE6HL0Vs+Xsh/CMXMjgXzz3JOgH4d/kw6VnghVg5RXOeLOiCmVyHaOlW8Jz\nImI26PbLVHRHjOvVvTuWKvPHhJY72+Ox6oYvOv3iDz4eywpeFOFr9N60aOs6t9IR\n2PZNMnAL9j4vC6BXxs0I4FGu6TF0LJHraf2MgnXoAQKBgQDwQHttFyhyaFMu0xPk\nyiXc9x4Ww+o4uB8AjLDmOlt9M+JZSyG8dnjaWg4R8Nxk5lHN2zeFm+uzK1kR5Nmk\nEIf9ldCjecoo3TeMNBIZte6mWZW7ljSx4HYm4AYzsjd+f1tGUmTzEJCaoTxZSBkP\nW5jmr5BObofHZ40YU+ORPXT2UQKBgQDsWhtzLCAgGjf7Y7xG5YOLKiiQKwJ4xeIs\nVI7+SOWyyrbtGp4J0FCkUWe432AJ6qBCcu6TTtiWatXb04NTbo0BRGIhOUP3pJQB\ngGYZkuzWsv400+PNh+ZQsFrMCs70yOTd4GdHMuL9O8rX2Q1ewv2avdfvUhNG+KMD\nksPP0iWrqQKBgQDi2mAw/97nOG7jFdgA/oeF/6jfoho1eFV9tVsL6SqeLDGcUv8F\n72/p7YK/mgjhFUFE+auRc0q5oUK3TLnc2uctoRqiYctrjoZ20mwM7ubrGEf0Gr6i\n/ulRh9MTWUJhJWxQGFjN0mRYPcq4GwXepITZvgiqpl96/+IQiJWmfLtGIQKBgQDh\nZynIk+trUjXTfJFhN59VB/a5TxtDXMzPJDFe1tygv2znALx5dX6CxtPZXsZzjpwZ\n4wwd1lL+WJLt23DiD4tQCwxezQNB2GYCbJZyi0ltlDSU4wLcz19Z0mY1M5Wdoz2J\nUGqOXzxU70IKyghTODit66FUrnyN8a9dSAmQV8TvSQKBgGjF7EUfLGEvXg8JmOKY\n4BkDqfdhXeLys5TCqr+aIzuYRjUM8P/t5nEkfzsX4qWvIsst+4uY3ZB8QbOVTyci\n5KPuZxMF/7WcCOf1St8Ye0Ung2IBDTZv0aI6l2nm58LlzI1Dv0srM677UugCNAFN\nShpVubiNYwGyJROsB5qKeiE3\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-apb5k@tsc-erp.iam.gserviceaccount.com",
  "client_id": "103742011116935524253",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-apb5k%40tsc-erp.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)
db = firestore.client()

UI_newcustomer = uic.loadUiType("ui_customer.ui")[0]
UI_savedialog = uic.loadUiType("dialog_companysave.ui")[0]

class NewCustomer(QDialog,UI_newcustomer):
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.buttonNewcustomer.clicked.connected(self.setData())

    def initUI(self):
        self.setupUi(self)
        self.saveButton.clicked.connect(lambda:self.setData())
        self.cancleButton.clicked.connect(lambda:self.close())
    #
    # def endInput(self):
    #     self.close

    def setData(self):
        temp_data = {'address':self.edit_address.text(),'TEL':self.edit_tel.text(),'FAX':self.edit_fax.text()
                     ,'delivery 1':self.edit_delivery1.text(),'delivery 2':self.edit_delivery2.text()}
        # print(temp_data)
        # companyName = self.edit_company.text()
        # print(companyName)
        # new_company_ref = db.collection('CUSTOMERS').document(companyName)
        # new_company_ref.set(temp_data)
        self.savedialog = SaveDialog()
        # self.savedialog.displayInfo()
        self.savedialog.name = self.edit_company.text()
        self.savedialog.datas = temp_data
        self.savedialog.exec_()
        self.close()

class SaveDialog(QDialog,UI_savedialog):
    name = None
    datas = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.buttonYes.clicked.connect(lambda:self.sendData())
        self.buttonNo.clicked.connect(lambda:self.close())

    def sendData(self):
        db.collection('CUSTOMERS').document(self.name).set(self.datas)
        self.close()

    def displayInfo(self):
        self.show()

#
# dialog = NewCustomer()
# dialog.show()
# app.exec_()