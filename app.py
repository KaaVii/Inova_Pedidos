import fix_qt_import_error
from exceptions import ValidationError
from services import (get_simafic_as_dataframe, get_main_icon, get_h_size, get_v_size, get_all_pedidos, add_pedido,validateCadastro,ValidationError)
from assets.style import getStyle
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QSortFilterProxyModel, pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog,QMainWindow, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QFormLayout,
                             QVBoxLayout, QWidget, QErrorMessage, QTableView, QSpacerItem, QListWidget, QListWidgetItem, QStyle)


main_icon = str(get_main_icon())
h_size=int(get_h_size())
v_size=int(get_v_size())

style = getStyle()



class CadastroPedidos(QDialog):

    def __init__(self, parent=None):
        super(CadastroPedidos, self).__init__(parent)

        self.setMinimumSize(QSize(h_size, v_size))
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QIcon(main_icon))
        self.setWindowTitle("Cadastro de Pedidos")
        self.setStyleSheet(style)

       #Sempre que for iniciado criará um objeto data
        self.data = dict()
        
        voltar_btn = QPushButton(self)
        voltar_btn.setText('Voltar')
        voltar_btn.clicked.connect(self.goMainWindow)

        self.dadosDoPedido()
        self.resumoGeral()
        self.resumoDosItens()
       
        '''disableWidgetsCheckBox.toggled.connect(
            self.bottomLeftGroupBox.setHidden
        )
        '''

        topLayout = QHBoxLayout()
        topLayout.addWidget(voltar_btn)


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
   
    def dadosDoPedido(self):
        self.topLeftGroupBox = QGroupBox("Dados do Pedido")

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        formLayout = QFormLayout()
        self.pedido = QLineEdit(self)
        self.pedido.setPlaceholderText("ex: 2112")
        pedido_label = QLabel("Pedido:")

        self.n_simafic = QLineEdit(self)
        self.n_simafic.setPlaceholderText("ex: 08.04.02.507-6")
        n_simafic_label = QLabel("Numero SIMAFIC:")

        self.qtd_items = QLineEdit(self)
        self.qtd_items.setPlaceholderText("ex: 100")
        qtd_items_label = QLabel("Quantidade de Items:")

        '''ADD PEDIDO'''
        add_item = QPushButton('Adicionar Item', self)
        add_item.setObjectName('Add')
        add_item.setIcon(QIcon('assets/check_icon_blue2.png'))
        add_item.clicked.connect(self.add_items)

        '''CLEAR BUTTON CONFIG '''
        clear_btn = QPushButton('Limpar Campos', self)
        clear_btn.setObjectName('Yellow')
        clear_btn.setIcon(QIcon('assets/eraser.png'))
        clear_btn.clicked.connect(self.pedido.clear)
        clear_btn.clicked.connect(self.n_simafic.clear)
        clear_btn.clicked.connect(self.qtd_items.clear)

        
        formLayout.addRow(pedido_label, self.pedido)
        formLayout.addRow(n_simafic_label, self.n_simafic)
        formLayout.addRow(qtd_items_label, self.qtd_items)
        formLayout.addItem(verticalSpacer)
        formLayout.addRow(add_item)
        formLayout.addRow(clear_btn)
 
        '''checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)'''

        #layout.addWidget(checkBox)
        '''formLayout.addWidget(add_item)
        formLayout.addWidget(clear_btn)'''
        


        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addStretch(2)
         
        self.topLeftGroupBox.setLayout(layout)

    def resumoGeral(self):
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

    def resumoDosItens(self):
        self.bottomLeftGroupBox = QGroupBox("Lista de Itens do Pedido nº")
        
        self.listDataItens = list()
        self.listaViewItens=QListWidget()

        removeSelected = QPushButton('Remover Itens Selecionados')
        removeSelected.clicked.connect(self.removerItens)

        layout = QGridLayout()
        layout.addWidget(removeSelected)
        
        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.bottomLeftGroupBox.setLayout(layout)

    def add_items(self):
        try:
            pedido, n_simafic, qtd_items = self.pedido.text(), self.n_simafic.text(), self.qtd_items.text()
            if validateCadastro(self.pedido.text(), self.n_simafic.text(), self.qtd_items.text()):
                print ("Validação concluída...")
                print ("Add Pedido: {} {} {}".format(self.pedido.text(), self.n_simafic.text(), self.qtd_items.text()))
                add_pedido(pedido, n_simafic, qtd_items)
        except ValidationError as error:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle(error.errors)
            error_dialog.setWindowIcon(QIcon(main_icon))
            error_dialog.showMessage(error.message)
            error_dialog.exec_()
        
        pass
        #add_pedido(pedido)

    def removerItens(self):
        listItems=self.listaViewItens.selectedItems()
        if not listItems: return        
        for item in listItems:
            print (type(item), dir(item))

    def goMainWindow(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Inove App"
        self.setMinimumSize(QSize(h_size, v_size))
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QtGui.QIcon(main_icon))
        self.setWindowTitle("Inove")
        self.setStyleSheet(style)
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())


        styleLabel = QLabel("&Estilo:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox(
            "&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")


        styleComboBox.activated[str].connect(self.changeStyle)
        '''self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(
            self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(
            self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(
            self.bottomLeftGroupBox.setDisabled
        )'''
        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)
        
        font = QFont()
        font.setPointSize(20)

        #layout = QHBoxLayout()
        cadastrarNovoPedidoBtn = QPushButton('Cadastrar Novo Pedido', self)
        cadastrarNovoPedidoBtn.setObjectName('Blue')
        cadastrarNovoPedidoBtn.setFont(font)
        cadastrarNovoPedidoBtn.setIcon(QIcon('assets/cadastro_blue.png'))
        cadastrarNovoPedidoBtn.setIconSize(QSize(40, 40))
        cadastrarNovoPedidoBtn.clicked.connect(self.cadastrarPedido)
        efetuarOperacaoLogBtn = QPushButton('Operação Logística', self)
        efetuarOperacaoLogBtn.setObjectName('Green')
        efetuarOperacaoLogBtn.setFont(font)
        efetuarOperacaoLogBtn.setIcon(QIcon('assets/logistica_green.png'))
        efetuarOperacaoLogBtn.setIconSize(QSize(40,40))
        efetuarOperacaoLogBtn.clicked.connect(self.operacaoLogistica)


        efetuarOperacaoLogBtn.resize(200,200)
        efetuarOperacaoLogBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cadastrarNovoPedidoBtn.resize(200,200)
        cadastrarNovoPedidoBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QGridLayout()
        layout.addLayout(topLayout, 0, 0, 1, 2)
        layout.addWidget(cadastrarNovoPedidoBtn,1,0)
        layout.addWidget(efetuarOperacaoLogBtn,1,1)
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(layout)
        self.show()

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
        self.setMinimumSize(QSize(h_size, v_size))
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
            itemclicked = w.itemDoubleClicked.connect(lambda item: self.simaficSelecionado(item))

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
        self.setMinimumSize(QSize(h_size, v_size))
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




   ''' def createBottomRightGroupBox(self):
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
        self.bottomRightGroupBox.setLayout(layout)'''
