import fix_qt_import_error
from services import get_simafic_as_dataframe, get_main_icon, get_h_size, get_v_size, get_all_pedidos
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QSortFilterProxyModel
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QErrorMessage, QTableView, QSpacerItem)


main_icon = str(get_main_icon())
h_size=int(get_h_size())
v_size=int(get_v_size())

class InoveApp(QDialog):

    def __init__(self, parent=None):
        super(InoveApp, self).__init__(parent)

        self.setMinimumSize(QSize(h_size, v_size))
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QtGui.QIcon(main_icon))
        self.setWindowTitle("Inove")

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox(
            "&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        # self.createBottomRightGroupBox()
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(
            self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(
            self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(
            self.bottomLeftGroupBox.setDisabled
        )

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.topLeftGroupBox, 50)
        leftLayout.addWidget(self.bottomLeftGroupBox, 50)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addLayout(leftLayout, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.changeStyle('windowsvista')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        print(styleName)
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)
            '''
            try:
                raise ValueError('A very specific bad thing happened.')
            except ValueError as error:
                error_dialog = QErrorMessage()
                error_dialog.setWindowIcon(main_icon)
                error_dialog.showMessage('Oh no!')
                error_dialog.exec_()
            '''

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Dados do Pedido")

        pedido = QLineEdit(self)
        pedido.setPlaceholderText("Numero do Pedido")
        n_simafic = QLineEdit(self)
        n_simafic.setPlaceholderText("Numero SIMAFIC")
        qtd_items = QLineEdit(self)
        qtd_items.setPlaceholderText("Qtd. de Items")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)


        '''ADD PEDIDO'''
        add_pedido = QPushButton('Adicionar Item', self)
        #Ainda falta conectar o submit
        #submit_btn.clicked.connect()
        add_pedido.setStyleSheet('QPushButton { font-weight: bold; color: blue;}')

        '''SUBMIT BUTTON CONFIG'''
        submit_btn = QPushButton('Prosseguir com o Scan', self)
        #Ainda falta conectar o submit
        #submit_btn.clicked.connect()
        submit_btn.setStyleSheet('QPushButton { font-weight: bold; color: green;}')

        '''CLEAR BUTTON CONFIG '''
        clear_btn = QPushButton('Limpar Campos', self)
        clear_btn.setStyleSheet('QPushButton { font-weight: bold; color: red;}')
        clear_btn.clicked.connect(pedido.clear)
        clear_btn.clicked.connect(n_simafic.clear)
        clear_btn.clicked.connect(qtd_items.clear)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(pedido)
        layout.addWidget(n_simafic)
        layout.addWidget(qtd_items)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        layout.addWidget(add_pedido)
        layout.addStretch(1)
        layout.addWidget(submit_btn)
        layout.addStretch(1)
        layout.addWidget(clear_btn)
        layout.addStretch(2)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QTabWidget()
        self.topRightGroupBox.setSizePolicy(QSizePolicy.Preferred,
                                            QSizePolicy.Ignored)
                                            


         #[First Tab] Create first tab
        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        tab1ListaItens = QWidget()
        layout = QVBoxLayout(self)

        #[First Tab] - Search Input
        searchPedido = QLineEdit(self)
        searchPedido.setPlaceholderText("Filtrar pedido: ")

        #[First Tab] - Set TableView
        

        table2Widget = QTableView()
        tab2hbox = QHBoxLayout()
        modelAllPedidos = get_all_pedidos()

        proxyPedidoFilter = QSortFilterProxyModel()
        proxyPedidoFilter.setSourceModel(modelAllPedidos)
        proxyPedidoFilter.setFilterKeyColumn(5)
        proxyPedidoFilter.setSortCaseSensitivity(Qt.CaseSensitive)
        #tab2hbox.setContentsMargins(5, 5, 5, 5)

        
       
        table2Widget.resizeColumnsToContents()
        table2Widget.setColumnWidth(2, 100)
        tab2hbox.addWidget(table2Widget)

        searchPedido.textChanged.connect(lambda wildcard: proxyPedidoFilter.setFilterWildcard(wildcard))
        table2Widget.setModel(proxyPedidoFilter)

        
        #[First Tab] - Set Layout
        layout.addWidget(searchPedido)
        layout.addWidget(table2Widget)
        layout.addItem(verticalSpacer)
        tab1ListaItens.setLayout(layout)

      
        tabItensValidos = QWidget()
        tableItensValidos = QTableView()
        #tableItensValidos.horizontalHeader().sectionClicked.connect(your_callable)

        model = get_simafic_as_dataframe()
        tableItensValidos.setModel(model)
        
        tab1hbox = QHBoxLayout()
        #tab1hbox.setContentsMargins(5, 5, 5, 5)
        tableItensValidos.resizeColumnsToContents()
        tab1hbox.addWidget(tableItensValidos)
        
        tabItensValidos.setLayout(tab1hbox)



      
        self.topRightGroupBox.addTab(tab1ListaItens, "&Lista de Pedidos: ")
        self.topRightGroupBox.addTab(tabItensValidos, "Itens de Itens:")

    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox("Resumo")
        
        output_pedido = QLineEdit()
        output_pedido.setReadOnly(True)
        output_pedido.setText('12345')
        #output_pedido.setDisabled(True)

        output_produto = QLineEdit()
        output_produto.setReadOnly(True)
        output_produto.setText('12345')
        #output_produto.setDisabled(True)

        output_desc = QLineEdit()
        output_desc.setReadOnly(True)
        output_desc.setText('12345')
        #output_desc.setDisabled(True)

        output_qtd_scanneada = QLineEdit()
        output_qtd_scanneada.setReadOnly(True)
        output_qtd_scanneada.setText('12345')
        #output_qtd_scanneada.setDisabled(True)

        output_qtd_total = QLineEdit()
        output_qtd_total.setReadOnly(True)
        output_qtd_total.setText('12345')
        #output_qtd_total.setDisabled(True)

        id_pedido_label = QLabel("&Numero do Pedido: ")
        id_pedido_label.setBuddy(output_pedido)
        id_produto_label =QLabel("&Produto: ")
        id_produto_label.setBuddy(output_pedido)
        desc_label = QLabel("&Desc: ")
        desc_label.setBuddy(output_desc)
        qty_scanneada = QLabel("&Qtd Scanneada.: ")
        qty_scanneada.setBuddy(output_qtd_scanneada)
        qty_total = QLabel("&Qtd Total: ")
        qty_total.setBuddy(output_qtd_total)

        layout = QGridLayout()
        
        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)


        layout.addWidget(id_pedido_label, 0, 0)
        layout.addWidget(output_pedido, 1, 0)
        layout.addWidget(id_produto_label, 0, 1)
        layout.addWidget(output_produto, 1, 1)
        layout.addWidget(desc_label, 2,0)
        layout.addWidget(output_desc, 3,0)
        layout.addWidget(qty_scanneada, 2, 1)
        layout.addWidget(output_qtd_scanneada, 3, 1)
        layout.addWidget(qty_total, 2, 2)
        layout.addWidget(output_qtd_total, 3, 2)
        layout.addItem(verticalSpacer, 6, 0, Qt.AlignTop)
        


        self.bottomLeftGroupBox.setLayout(layout)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = InoveApp()
    gallery.show()
    #gallery.showMaximized()
    sys.exit(app.exec_())
