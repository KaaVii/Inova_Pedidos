import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMain
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    

class MainView(self):
    
    def __init__(self):

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,32)
        pybutton.move(80, 60)        

    def clickMethod(self):
        print('Your name: ' + self.line.text())

if __name__ == "__main__":
    print("Views Module called by main method")
else:
    print("Calling Views module")