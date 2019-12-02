from PyQt5 import QtWidgets,QtCore
import sys
import os
class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()
        self.mylineEdit = QtWidgets.QLineEdit()
        self.mylineEdit2 = QtWidgets.QLineEdit()
        self.startNew=1
        #initialise to empty string on start up
        self.mylineEdit.setText('')


        #barcode scans here and then a returnPressed is registered

        #connect to a function
        self.mylineEdit.returnPressed.connect(self.set_sample_name) #here is where I want to delete the previous entry without backspacing by hand
        self.mylineEdit.textChanged.connect(self.delete_previous)

        centwid=QtWidgets.QWidget()
        lay=QtWidgets.QVBoxLayout()
        lay.addWidget(self.mylineEdit)
        lay.addWidget(self.mylineEdit2)
        centwid.setLayout(lay)
        self.setCentralWidget(centwid)
        self.show()

        #set the sample name variable
    def set_sample_name(self):
        self.sample_name = self.mylineEdit.text()
        print(self.sample_name)
        self.startNew=1
    def delete_previous(self,text):
        if self.startNew:
            self.mylineEdit.setText(text[-1])
            self.startNew=0
app=QtWidgets.QApplication(sys.argv)
ex=window()
sys.exit(app.exec_())