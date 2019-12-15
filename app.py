import fix_qt_import_error
from exceptions import ValidationError
from services import (get_simafic_as_dataframe, get_main_icon, get_h_size, get_v_size, get_all_pedidos_pandas, add_pedido,validateCadastro,
validateInfoScan,ValidationError, get_all_pedidos)
from assets.style import getStyle
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QSortFilterProxyModel, pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog,QMainWindow, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,QMessageBox,
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
        n_simafic_label = QLabel("COD. SIMAFIC:")

        self.qtd_items = QLineEdit(self)
        self.qtd_items.setPlaceholderText("ex: 100")
        qtd_items_label = QLabel("Quantidade de Items:")

        '''ADD PEDIDO'''
        add_item = QPushButton('Adicionar Item')
        add_item.setObjectName('Add')
        add_item.setIcon(QIcon('assets/check_icon_blue2.png'))
        add_item.clicked.connect(self.add_items)

        '''CLEAR BUTTON CONFIG '''
        clear_btn = QPushButton('Limpar Campos')
        clear_btn.setObjectName('Yellow')
        clear_btn.setIcon(QIcon('assets/eraser.png'))
        clear_btn.clicked.connect(self.limpar_pedidos)
                
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
        tab1ListaPedidos = QWidget()
        layout = QVBoxLayout(self)

        #[First Tab] - TextFields
        searchPedido = QLineEdit(self)
        searchPedido.setPlaceholderText("Filtrar por pedido: ")
        searchProduto = QLineEdit(self)
        searchProduto.setPlaceholderText("Filtrar por produto: ")


        #[First Tab] - Set TableView
        tabv_pedidos = QTableView()
        tab2hbox = QHBoxLayout()
        self.modelAllPedidos = get_all_pedidos_pandas()

        #[First Tab] - Set Filters
        self.proxyPedidoFilter = QSortFilterProxyModel()
        self.proxyPedidoFilter.setSourceModel(self.modelAllPedidos)
        self.proxyPedidoFilter.setFilterKeyColumn(0)
        self.proxyPedidoFilter.setSortCaseSensitivity(Qt.CaseSensitive)
        self.proxyPedidoFilterSecondLayer = QSortFilterProxyModel()
        self.proxyPedidoFilterSecondLayer.setSourceModel(self.proxyPedidoFilter)
        self.proxyPedidoFilterSecondLayer.setFilterKeyColumn(1)
        self.proxyPedidoFilterSecondLayer.setSortCaseSensitivity(Qt.CaseSensitive)
        
        
       
        tabv_pedidos.resizeColumnsToContents()
        tabv_pedidos.setColumnWidth(2, 100)
        tabv_pedidos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tab2hbox.addWidget(tabv_pedidos)


        #[Connect Fields]
        searchProduto.textChanged.connect(lambda wildcard: self.proxyPedidoFilterSecondLayer.setFilterWildcard(wildcard))
        searchPedido.textChanged.connect(lambda wildcard: self.proxyPedidoFilter.setFilterWildcard(wildcard))
        tabv_pedidos.setModel(self.proxyPedidoFilterSecondLayer)
        tabv_pedidos.resizeColumnsToContents
        tabv_pedidos.resizeRowsToContents
         

        
        #[First Tab] - Set Layout
        

      
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

        layoutText = QHBoxLayout()
        layoutText.addWidget(searchPedido)
        layoutText.addWidget(searchProduto)
        
        layout.addLayout(layoutText)
        layout.addWidget(tabv_pedidos)
        tab1ListaPedidos.setLayout(layout)
      

        self.topRightGroupBox.addTab(tab1ListaPedidos, "&Lista de Pedidos: ")
        self.topRightGroupBox.addTab(tabItensValidos, "&Lista de Itens:")

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
                print ("Add Pedido: {} {} {}".format(pedido, n_simafic, qtd_items))
                mb = QMessageBox()
                mb.setIconPixmap(QPixmap('assets/check_icon_blue2'))
                mb.setWindowTitle("Sucesso")
                mb.setText('O pedido: {} foi criado com sucesso!'.format(pedido))
                mb.exec_()
                add_pedido(pedido, n_simafic, qtd_items)
                self.limpar_pedidos()
                

        except ValidationError as error:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle(error.errors)
            error_dialog.setWindowIcon(QIcon(main_icon))
            error_dialog.showMessage(error.message)
            error_dialog.exec_()
        
        pass
        #add_pedido(pedido)
    
    



    def limpar_pedidos(self):
        self.n_simafic.clear()
        self.qtd_items.clear()
        self.pedido.clear()

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
        cadastrarNovoPedidoBtn = QPushButton('Cadastrar Novo Pedido')
        cadastrarNovoPedidoBtn.setObjectName('Blue')
        cadastrarNovoPedidoBtn.setFont(font)
        cadastrarNovoPedidoBtn.setIcon(QIcon('assets/cadastro_blue.png'))
        cadastrarNovoPedidoBtn.setIconSize(QSize(40, 40))
        cadastrarNovoPedidoBtn.clicked.connect(self.cadastrarPedido)
        efetuarOperacaoLogBtn = QPushButton('Operação Logística')
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
        self.setWindowIcon(QIcon(main_icon))

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)


        #Pedido Input Field
        self.numero_pedido = QLineEdit(self)
        self.numero_pedido.setPlaceholderText("Insira o Número do Pedido")


        #Procurar Pedido Btn
        self.procurar_pedido_btn = QPushButton("Procurar Pedido")
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


        #Adicionar Cores no StyleSheet
        colors = ['##393318', '  ##fff']
        pedidos = get_all_pedidos()

        w = QListWidget()
        for pedido in pedidos:
            i = QListWidgetItem('{}'.format(pedido.desc))
            if( 2 % 2 ==0):
                i.setBackground( QColor('#c8ccd0') )
            else:
                i.setBackground( QColor('#ffffff') )
            w.addItem(i)
        w.itemDoubleClicked.connect(lambda item: self.simaficSelecionado(item))
        
        layout = QGridLayout()
        layout.addWidget(self.numero_pedido,0,0)
        layout.addWidget(self.procurar_pedido_btn,0,1)
        layout.addWidget(self.voltar_btn,0,2)
        layout.addWidget(w,1,0,1,3)
        self.setLayout(layout)

    def simaficSelecionado(self, value):
        print (value.text())
        self.cams = ItemScanner(value.text(), "Eu sou o Simafic", "Eu sou a Descrição", "300")
        self.cams.show()
        self.close()

    def goMainWindow(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close()

    def goScan(self):
        self.cams = ItemScanner("Eu sou o Pedido", "Eu sou o Simafic", "Eu sou a Descrição", "300")
        self.cams.show()
        self.close()


class ItemScanner(QDialog):
    def __init__(self, pedido, simafic, desc, qtd_total, parent=None):
        super().__init__(parent)
        self.pedido, self.simafic, self.desc, self.qtd_total = pedido, simafic, desc, qtd_total
        self.font = QFont()
        self.fontScan = QFont()
        self.fontScan.setPointSize(14)
        self.font.setPointSize(16)

        self.setStyleSheet('assets/style.py')
        self.setWindowTitle('Scanner')
        self.setWindowIcon(QIcon(main_icon))
        self.setMinimumSize(QSize(h_size, v_size))
        label1 = QLabel(pedido)
        voltar_btn = QPushButton('Voltar')
        voltar_btn.clicked.connect(self.goOperacoesLogisticas)

        titleLabel = QLabel('Pedido Nº {pedido}'.format(pedido=pedido))
        titleLabel.setFont(self.font)        
        titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setObjectName('ScanTitle')


        vLayout= QVBoxLayout()
        self.createPedidoInfo()
        self.createCountElement()
        
        vLayout.setContentsMargins(30,30,30,30)

        vLayout.addWidget(voltar_btn)
        vLayout.addStretch(1)
        vLayout.addWidget(titleLabel)
        vLayout.addWidget(self.pedidoInfoBox)
        vLayout.addStretch(1)
        vLayout.addWidget(self.countElementGroupBox)
        vLayout.addStretch(2)
        
        

        '''gridLayout = QGridLayout()

        gridLayout.addWidget(titleLabel, 0,1)
        gridLayout.addLayout(scanLayout, 1,1)'''

        vLayout.setAlignment(Qt.AlignCenter)

        self.setLayout(vLayout)

    def createPedidoInfo(self):
        self.pedidoInfoBox = QGroupBox()
        finalInfoLayout = QVBoxLayout()
        scanInfoLayout = QFormLayout()

        self.count_resp = QLineEdit(self)
        self.count_resp.setPlaceholderText("ex. John Doe")

        self.id_caixa = QLineEdit(self)
        self.id_caixa.setPlaceholderText("ex. 12AB")

        desc_le = QLineEdit('Descrição')
        desc_le.setText = self.desc
        desc_le.setReadOnly(True)
        desc_le.setDisabled(True)

        simafic = QLineEdit('COD. SIMAFIC')
        simafic.setText = simafic
        simafic.setReadOnly(True)
        simafic.setDisabled(True)

        #scanLayout.addWidget(self.voltar_btn)
        scanInfoLayout.addRow("Descrição:", desc_le)
        scanInfoLayout.addRow("COD. SIMAFIC:", simafic)
        scanInfoLayout.addRow("Responsável pela contagem:", self.count_resp)
        scanInfoLayout.addRow("Numero da Caixa:", self.id_caixa)
        scanInfoLayout.setContentsMargins(75,75,75,10)

        buttonsLayout = QHBoxLayout()

        self.startCount = QPushButton('Confirmar')
        self.startCount.clicked.connect(self.validaPedidoInfo)

        cancelarCount = QPushButton('Cancelar')
        cancelarCount.clicked.connect(self.cancelarScan)

        buttonsLayout.setContentsMargins(75,10,75,20)


        buttonsLayout.addWidget(self.startCount)
        buttonsLayout.addWidget(cancelarCount)

        finalInfoLayout.addLayout(scanInfoLayout)
        finalInfoLayout.addLayout(buttonsLayout)

        self.pedidoInfoBox.setLayout(finalInfoLayout)

        pass;

    def createCountElement(self):
        self.countElementGroupBox = QGroupBox()
        scanLayout = QVBoxLayout()
        hCountLayout = QHBoxLayout()
       
        qtd_parcial_label = QLabel('Qtd. Atual:')
        qtd_total_label = QLabel('Qtd. Total:')
        qtd_total_label.setFont(self.font)
        qtd_parcial_label.setFont(self.font)

        qtd_parcial_le = QLineEdit()
        qtd_total_le = QLineEdit()
        qtd_total_le.setFont(self.font)
        qtd_parcial_le.setFont(self.font)
        qtd_parcial_le.setText(str(0))
        qtd_parcial_le.setReadOnly(True)
        qtd_total_le.setText(str(self.qtd_total))
        qtd_total_le.setReadOnly(True)

        qtd_parcial_label.setBuddy(qtd_parcial_le)
        qtd_total_label.setBuddy(qtd_parcial_le)

        input_scan_label = QLabel('Scanneie o COD. SIMAFIC do Produto:')
        input_scan_label.setFont(self.fontScan)
        input_scan_label.setAlignment(Qt.AlignCenter)
        input_scanner = QLineEdit()
        input_scanner.setAlignment(Qt.AlignCenter)
        input_scanner.setFont(self.fontScan)
        input_scan_label.setBuddy(input_scanner)

        hCountLayout.addStretch(1)
        hCountLayout.addWidget(qtd_parcial_label)
        hCountLayout.addWidget(qtd_parcial_le)
        hCountLayout.addStretch(1)
        hCountLayout.addWidget(qtd_total_label)
        hCountLayout.addWidget(qtd_total_le)
        hCountLayout.addStretch(1)
        hCountLayout.setContentsMargins(0,30,0,0)
        scanLayout.setContentsMargins(75,20,75,75)

    
        scanLayout.addWidget(input_scan_label)
        scanLayout.addWidget(input_scanner)
        scanLayout.addStretch(1)
        scanLayout.addLayout(hCountLayout)
        scanLayout.addStretch(3)

        self.countElementGroupBox.setLayout(scanLayout)
        self.countElementGroupBox.setDisabled(True)

    
    def validaPedidoInfo(self):
        try:
            print ("validateInfoScan")
            print ("Validando campos... {} {}".format(self.count_resp.text, self.id_caixa.text))
            validateInfoScan(self.count_resp.text(), self.id_caixa.text())
            self.startCount.setDisabled(True)
            self.count_resp.setDisabled(True)
            self.id_caixa.setDisabled(True)
            self.countElementGroupBox.setDisabled(False)

        except ValidationError as error:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle(error.errors)
            error_dialog.setWindowIcon(QIcon(main_icon))
            error_dialog.showMessage(error.message)
            error_dialog.exec_()
       
        
    def cancelarScan(self):
        print("Cancelar Scan")
        
    def goOperacoesLogisticas(self):
        self.cams = OperacaoLogistica()
        self.cams.show()
        self.close()

    def goMainWindow(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close() 

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainView = MainWindow()
    mainView.show()
    
    #gallery.show()
    #gallery.showMaximized()
    sys.exit(app.exec_())
    callSuccessMsgBox('teste', 'teste')


def teste():
    print('teste')
    pass

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
