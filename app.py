import fix_qt_import_error
from services import get_simafic_as_dataframe, get_main_icon, get_h_size, get_v_size, get_all_pedidos, add_pedido
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QSortFilterProxyModel, pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog,QMainWindow, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QErrorMessage, QTableView, QSpacerItem)


main_icon = str(get_main_icon())
h_size=int(get_h_size())
v_size=int(get_v_size())

class CadastroPedidos(QDialog):

    def __init__(self, parent=None):
        super(CadastroPedidos, self).__init__(parent)

        self.setMinimumSize(QSize(h_size, v_size))
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QtGui.QIcon(main_icon))
        self.setWindowTitle("Inove")

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Estilo:")
        styleLabel.setBuddy(styleComboBox)
        
        voltar_btn = QPushButton(self)
        voltar_btn.setText('Voltar')
        voltar_btn.clicked.connect(self.goMainWindow)


        self.useStylePaletteCheckBox = QCheckBox(
            "&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createSubmitButtons()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(
            self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(
            self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(
            self.bottomLeftGroupBox.setDisabled
        )
        '''disableWidgetsCheckBox.toggled.connect(
            self.bottomLeftGroupBox.setHidden
        )
        '''
        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addWidget(voltar_btn)
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
        #mainLayout.addWidget(self.submitButtons, 3, 0, 1, 2)
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

   
    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Dados do Pedido")

        firstLayout = QHBoxLayout()
        pedido = QLineEdit(self)
        pedido.setPlaceholderText("Numero do Pedido")

        firstLayout.addWidget(pedido)

        n_simafic = QLineEdit(self)
        n_simafic.setPlaceholderText("Numero SIMAFIC")
        qtd_items = QLineEdit(self)
        qtd_items.setPlaceholderText("Qtd. de Items")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)


        '''ADD PEDIDO'''
        add_item = QPushButton('Adicionar Item', self)
        #Ainda falta conectar o submit
        #submit_btn.clicked.connect()
        add_item.setStyleSheet('QPushButton { font-weight: bold; color: blue;}')

        '''SUBMIT BUTTON CONFIG'''
        #submit_btn = QPushButton('Prosseguir com o Scan', self)
        #Ainda falta conectar o submit
        #submit_btn.clicked.connect()
        #submit_btn.setStyleSheet('QPushButton { font-weight: bold; color: green;}')

        '''CLEAR BUTTON CONFIG '''
        clear_btn = QPushButton('Limpar Campos', self)
        clear_btn.setStyleSheet('QPushButton { font-weight: bold; color: red;}')
        clear_btn.clicked.connect(pedido.clear)
        clear_btn.clicked.connect(n_simafic.clear)
        clear_btn.clicked.connect(qtd_items.clear)

        '''checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)'''

        secondlayout = QVBoxLayout()

        secondlayout.addWidget(n_simafic)
        secondlayout.addWidget(qtd_items)
        #layout.addWidget(checkBox)
        secondlayout.addStretch(1)
        secondlayout.addWidget(add_item)
        secondlayout.addWidget(clear_btn)
        secondlayout.addStretch(2)


        layout = QVBoxLayout()
        layout.addLayout(firstLayout)
        layout.addLayout(secondlayout)
        
        
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QTabWidget()
        self.topRightGroupBox.setSizePolicy(QSizePolicy.Preferred,
                                            QSizePolicy.Ignored)
                                            


         #[First Tab] Create first tab
        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        tab1ListaItens = QWidget()
        layout = QVBoxLayout(self)

        #[First Tab] - TextFields
        searchPedido = QLineEdit(self)
        searchPedido.setPlaceholderText("Filtrar por pedido: ")
        searchProduto = QLineEdit(self)
        searchProduto.setPlaceholderText("Filtrar por produto: ")


        #[First Tab] - Set TableView
        table2Widget = QTableView()
        tab2hbox = QHBoxLayout()
        modelAllPedidos = get_all_pedidos()


        #[First Tab] - Set Filters
        proxyPedidoFilter = QSortFilterProxyModel()
        proxyPedidoFilter.setSourceModel(modelAllPedidos)
        proxyPedidoFilter.setFilterKeyColumn(0)
        proxyPedidoFilter.setSortCaseSensitivity(Qt.CaseSensitive)
        proxyProdutoFilter = QSortFilterProxyModel()
        proxyProdutoFilter.setSourceModel(proxyPedidoFilter)
        proxyProdutoFilter.setFilterKeyColumn(1)
        proxyProdutoFilter.setSortCaseSensitivity(Qt.CaseSensitive)

        
       
        table2Widget.resizeColumnsToContents()
        table2Widget.setColumnWidth(2, 100)
        tab2hbox.addWidget(table2Widget)


        #[Connect Fields]
        searchProduto.textChanged.connect(lambda wildcard: proxyProdutoFilter.setFilterWildcard(wildcard))
        searchPedido.textChanged.connect(lambda wildcard: proxyPedidoFilter.setFilterWildcard(wildcard))
        table2Widget.setModel(proxyProdutoFilter)

        
        #[First Tab] - Set Layout
        layoutText = QHBoxLayout()
        layoutText.addWidget(searchPedido)
        layoutText.addWidget(searchProduto)
        
        layout.addLayout(layoutText)
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
        self.bottomLeftGroupBox = QGroupBox("Itens do Pedido nº")
        
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

    def add_pedido(self, pedido):
        print ("Add Pedido {}".format(pedido))
        add_pedido(pedido)

    def createSubmitButtons(self):
        '''self.submitButtons = QGroupBox('Submit Buttons')
        layout = QHBoxLayout()
        adicionarpedido = QPushButton('&Confirmar Cadastro', self)
        cancelarpedido = QPushButton('&Cancelar Cadastro', self)
        layout.addWidget(adicionarpedido)
        layout.addWidget(cancelarpedido) 
        
        self.submitButtons.setLayout(submitButtons)'''
        pass

    def goMainWindow(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "App"
        self.setMinimumSize(QSize(640, 480))
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QtGui.QIcon(main_icon))
        self.setWindowTitle("Inove")
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        
        #layout = QHBoxLayout()
        cadastrarNovoPedidoBtn = QPushButton('Cadastrar Novo Pedido', self)
        cadastrarNovoPedidoBtn.setStyleSheet('QPushButton { font-weight: bold; color: blue;}')
        cadastrarNovoPedidoBtn.clicked.connect(self.cadastrarPedido)

        

        efetuarOperacaoLogBtn = QPushButton('Operação Logística', self)
        efetuarOperacaoLogBtn.setStyleSheet('QPushButton { font-weight: bold; color: green;}')
        efetuarOperacaoLogBtn.clicked.connect(self.operacaoLogistica)


        efetuarOperacaoLogBtn.resize(200,200)
        efetuarOperacaoLogBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cadastrarNovoPedidoBtn.resize(200,200)
        cadastrarNovoPedidoBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QGridLayout()
        layout.addWidget(cadastrarNovoPedidoBtn,0,0)
        layout.addWidget(efetuarOperacaoLogBtn,0,1)
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(layout)
        self.show()

    @pyqtSlot()
    def cadastrarPedido(self):
        self.statusBar().showMessage("Switched to CadastroPedidos")
        self.cams = CadastroPedidos() 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def operacaoLogistica(self):
        self.statusBar().showMessage("Switched to OperacaoLogistica")
        self.cams = OperacaoLogistica() 
        self.cams.show()
        self.close()
        

class OperacaoLogistica(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Operação Logística')
        self.setMinimumSize(QSize(640, 480))
        self.setWindowIcon(QtGui.QIcon(main_icon))

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)


        #Pedido Input Field
        self.numero_pedido = QLineEdit(self)
        self.numero_pedido.setPlaceholderText("Insira o Número do Pedido")


        #Procurar Pedido Btn
        self.procurar_pedido_btn = QPushButton("Procurar Pedido", self)
        self.procurar_pedido_btn.setIconSize(QSize(200, 200))
        self.procurar_pedido_btn.clicked.connect(self.goScan)

        #Voltar Btn
        self.voltar_btn = QPushButton(self)
        #self.voltar_btn.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.voltar_btn.setText('Voltar')
        self.voltar_btn.clicked.connect(self.goMainWindow)
        self.close()

        '''#Layout Vertical
        layoutV = QHBoxLayout()
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.numero_pedido)
        layoutH.addWidget(self.procurar_pedido_btn)
        layoutH.addWidget(self.voltar_btn)
        layoutV.addLayout(layoutH)
        layoutV.addItem(verticalSpacer)
        self.setLayout(layoutV)'''

        colors = ['##393318', '  ##fff']

        w = QListWidget()
        for n in range(8):
            i = QListWidgetItem('%s' % n)
            item = QListWidgetItem()
            text = "teste{}".format(1)
            item.setText(text)
            item.setData(n, text)
            
            if( n % 2 ==0):
                i.setBackground( QColor('#c8ccd0') )
            else:
                i.setBackground( QColor('#ffffff') )
            w.addItem(i)
            itemclicked = w.itemClicked.connect(lambda item: self.simaficSelecionado(item))

        #Layout Vertical
        layout = QGridLayout()
        layout.addWidget(self.numero_pedido,0,0)
        layout.addWidget(self.procurar_pedido_btn,0,1)
        layout.addWidget(self.voltar_btn,0,2)
        layout.addWidget(w)
        layout.addItem(verticalSpacer)
        self.setLayout(layout)

    def simaficSelecionado(self, value):
        print (value.text())

    def goMainWindow(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close()

    def goScan(self):
        self.cams = ItemScanner(self.numero_pedido.text())
        self.cams.show()
        self.close()


class ItemScanner(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Scanner')
        self.setMinimumSize(QSize(640, 480))
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        label1 = QLabel(value)
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.button.setIconSize(QSize(200, 200))

        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setText(value)
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)

        layoutH = QHBoxLayout()
        layoutH.addWidget(label1)
        layoutH.addWidget(self.button)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

    def goMainWindow(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close() 


'''
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=MainWindow()
    sys.exit(app.exec_())'''

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainView = MainWindow()
    mainView.show()
    
    #gallery.show()
    #gallery.showMaximized()
    sys.exit(app.exec_())
