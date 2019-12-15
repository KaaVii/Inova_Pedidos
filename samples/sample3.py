import sys, os
from PyQt5 import QtCore, QtGui
app=QtGui.QApplication(sys.argv)

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)
        self.items=['One','Two','Three','Four','Five','Six','Seven']

    def rowCount(self, parent=QtCore.QModelIndex()):   
        return len(self.items)
    def columnCount(self, index=QtCore.QModelIndex()):
        return 1

    def data(self, index, role):
        if not index.isValid() or not (0<=index.row()<len(self.items)):
            return QtCore.QVariant()

        item=str(self.items[index.row()])

        if role==QtCore.Qt.DisplayRole:
            return item
        else:
            return QtCore.QVariant()


class MySortFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        super(MySortFilterProxyModel, self).__init__()
        self.cb_status=True

    def cbChanged(self, arg=None):
        self.cb_status=arg
        print (self.cb_status)
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        print_when_odd_flag = self.cb_status
        is_odd = True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        print ("My Row Data: %s" % self.sourceModel().data(index, role=QtCore.Qt.DisplayRole))

        if (sourceRow + 1) % 2 == 0:
            is_odd = False

        if print_when_odd_flag:
            if is_odd:
                return True
            else:
                return False
        else:
            if not is_odd:
                return True
            else:
                return False


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        mainLayout=QtGui.QHBoxLayout()
        self.setLayout(mainLayout)   

        self.viewA=QtGui.QTableView()
        self.viewA.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch) 

        self.myModel=TableModel()

        self.sortModel = MySortFilterProxyModel()
        self.sortModel.setSourceModel(self.myModel)

        self.viewA.setModel(self.sortModel)

        self.checkBox=QtGui.QCheckBox("Show All")  
        self.checkBox.stateChanged.connect(self.sortModel.cbChanged)
        self.checkBox.setChecked(self.sortModel.cb_status)

        mainLayout.addWidget(self.viewA)
        mainLayout.addWidget(self.checkBox)  
        self.show()   

view=Window() 
sys.exit(app.exec_())