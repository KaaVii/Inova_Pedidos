import sys

from PySide import QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.resize(720, 480)
        central_widget = QtGui.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QtGui.QHBoxLayout(central_widget)

        self.text_edit = QtGui.QTextEdit(central_widget)
        layout.addWidget(self.text_edit)

        self.drop_list = QtGui.QListWidget(central_widget)
        self.drop_list.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.drop_list.addItems(['one', 'two', 'three', 'four'])
        self.drop_list.itemSelectionChanged.connect(self.show_List)
        layout.addWidget(self.drop_list)

        statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(statusbar)

        action_ShowList = QtGui.QAction(self)
        action_ShowList.triggered.connect(self.show_List)

        self.show()

    def show_List(self):
        self.text_edit.setText(repr(self.drop_list.selectedItems()))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    frame = MainWindow()
    sys.exit(app.exec_())