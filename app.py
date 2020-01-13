import fix_qt_import_error
from exceptions import ValidationError, DBPedidosException
import services
from assets.style import getStyle
from classes.pedidoTreeModel import PedidoItensTree
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QSortFilterProxyModel, pyqtSlot, QModelIndex, QStringListModel
from PyQt5 import QtGui
from datetime import datetime
import pprint
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, QAbstractItemView, QMessageBox,
                             QDial, QDialog,QMainWindow, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,QMessageBox, QListView,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QFormLayout,QTreeView,
                             QVBoxLayout, QWidget, QErrorMessage, QTableView, QSpacerItem, QListWidget, QListWidgetItem, QStyle, QHeaderView)
import time



class CadastroPedidos(QDialog):

    def __init__(self, parent=None):
        super(CadastroPedidos, self).__init__(parent=None)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)

        self.setMinimumSize(QSize(h_size, v_size))
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QIcon(main_icon))
        self.setWindowTitle("Cadastro de Pedidos")
        self.setStyleSheet(style)

        self.pedidos_selecionados = []

       #Sempre que for iniciado criará um objeto data
        self.data = dict()
        
        voltar_btn = QPushButton(self)
        voltar_btn.setText('Voltar')
        voltar_btn.clicked.connect(self.goMainWindow)
        voltar_btn.setFocusPolicy(Qt.NoFocus)


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
        leftLayout.addWidget(self.topLeftGroupBox, 100)
        #leftLayout.addWidget(self.bottomLeftGroupBox, 50)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addLayout(leftLayout, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        #mainLayout.addWidget(self.submitButtons, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 3)

        self.setLayout(mainLayout)

    def dadosDoPedido(self):
        self.topLeftGroupBox = QGroupBox("Dados do Pedido")

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        formLayout = QFormLayout()
        self.pedido = QLineEdit(self)
        self.pedido.setPlaceholderText("ex: 123.456")
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
        self.tabv_pedidos = QTableView()
        tab2hbox = QHBoxLayout()
        self.modelAllPedidos = services.get_all_pedidos_pandas()

        #[First Tab] - Set Filters
        self.proxyPedidoFilter = QSortFilterProxyModel()
        self.proxyPedidoFilter.setSourceModel(self.modelAllPedidos)
        self.proxyPedidoFilter.setFilterKeyColumn(0)
        self.proxyPedidoFilter.setSortCaseSensitivity(Qt.CaseSensitive)
        self.proxyPedidoFilterSecondLayer = QSortFilterProxyModel()
        self.proxyPedidoFilterSecondLayer.setSourceModel(self.proxyPedidoFilter)
        self.proxyPedidoFilterSecondLayer.setFilterKeyColumn(1)
        self.proxyPedidoFilterSecondLayer.setSortCaseSensitivity(Qt.CaseSensitive)
        
        
       
        self.tabv_pedidos.resizeColumnsToContents()
        self.tabv_pedidos.doubleClicked.connect(self.abrirItensDoPedido)
        self.tabv_pedidos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabv_pedidos.setSelectionBehavior(QTableView.SelectRows)


        self.tabv_pedidos.setColumnWidth(2, 100)
        self.tabv_pedidos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tab2hbox.addWidget(self.tabv_pedidos)


        #[Connect Fields]
        searchProduto.textChanged.connect(lambda wildcard: self.proxyPedidoFilterSecondLayer.setFilterWildcard(wildcard))
        searchPedido.textChanged.connect(lambda wildcard: self.proxyPedidoFilter.setFilterWildcard(wildcard))
        self.tabv_pedidos.setModel(self.proxyPedidoFilterSecondLayer)
       
        #[First Tab] - Set Layout
      
        tabItensValidos = QWidget()
        tableItensValidos = QTableView()
        #tableItensValidos.horizontalHeader().sectionClicked.connect(your_callable)

        model = services.get_simafic_as_dataframe()
        
        
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
        layout.addWidget(QLabel("Para abrir mais opções sobre um pedido, clique duas vezes no item."))
        
        self.tabv_pedidos.verticalHeader()
        self.tabv_pedidos.resizeColumnsToContents()
        layout.addWidget(self.tabv_pedidos)
        tab1ListaPedidos.setLayout(layout)
        
      

        #TODO: Agrupar items por pedido (Drop Down) | Auto-resize nas cells da TView
        #TODO: Adicionar

        self.topRightGroupBox.addTab(tab1ListaPedidos, "&Lista de Pedidos: ")
        self.topRightGroupBox.addTab(tabItensValidos, "&Lista de Itens:")

    def resumoDosItens(self):
        self.bottomLeftGroupBox = QGroupBox("Lista de Itens do Pedido nº")
        self.listDataItens = list()
        self.listaViewItens=QListWidget()

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.resumoLayout = QGridLayout()
        self.resumoLayout.addItem(verticalSpacer)
        self.bottomLeftGroupBox.setLayout(self.resumoLayout)

    def abrirItensDoPedido(self, item):
        print("[abrirIItensDoPedido] O Item foi selecionado através de um click na: {} x linha: {}".format(item.column(), item.row()))
        pedido = self.tabv_pedidos.model().index(item.row(), 0).data()
        simafic = self.tabv_pedidos.model().index(item.row(), 1).data()
        print(pedido, simafic)
        self.pedidos_selecionados = pedido

        try:
            pedido_item = services.get_pedido_x_item(pedido, simafic)
            print(pedido_item)
        except (ValidationError, DBPedidosException) as error:
            error_dialog = QErrorMessage()  
            error_dialog.setWindowTitle(error.errors)
            error_dialog.setWindowIcon(QIcon(main_icon))
            error_dialog.showMessage(error.message)
            error_dialog.exec_()

        box = QMessageBox()
        box.setWindowIcon(QIcon(main_icon))
        box.setWindowTitle("Pedido {} selecionado.".format(pedido_item.id_pedido))
        box.setText("O que deseja fazer com o item {}?".format(pedido_item.cod_simafic))
        box.setStandardButtons(QMessageBox.Open | QMessageBox.Discard | QMessageBox.Cancel)
        buttonOpen = box.button(QMessageBox.Open)
        buttonOpen.setText('Alterar')
        buttonDiscard = box.button(QMessageBox.Discard)
        buttonDiscard.setText('Excluir')
        buttonCancel = box.button(QMessageBox.Cancel)
        buttonCancel.setText('Cancelar')
        box.exec_()
        if box.clickedButton() == buttonOpen:
            print ("Alterar...")
            self.cams = UpdateScreen(pedido_item, parent=self)
            self.cams.show()
        elif box.clickedButton() == buttonDiscard:
            print ("Excluir ")
            self.confirmarExclusao(pedido_item)

        elif box.clickedButton() == buttonCancel:
            print ("Cancelar ")
            

    def confirmarExclusao(self, pedido):
        box = QMessageBox()
        box.setWindowIcon(QIcon(main_icon))
        box.setWindowTitle('Confirmação de Exclusão')
        box.setText("Tem certeza que deseja excluir o item: {} do pedido {}?".format(pedido.cod_simafic, pedido.id_pedido))
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonYes = box.button(QMessageBox.Yes)
        buttonYes.setText("Excluir")
        buttonNo = box.button(QMessageBox.No)
        buttonNo.setText("Cancelar")
        box.exec_()

        if box.clickedButton() == buttonYes:
            self.excluirPedido(pedido)
            print("Pedido excluido")
            
        else:
            print("Exclusão cancelada")
            return

    def excluirPedido(self, pedido):
        try:
            services.excluirPedidoItem(pedido)
            self.update_model_tableview()

        except (ValidationError, DBPedidosException) as error:
            error_dialog = QErrorMessage()  
            error_dialog.setWindowTitle(error.errors)
            error_dialog.setWindowIcon(QIcon(main_icon))
            error_dialog.showMessage(error.message)
            error_dialog.exec_()

    


    def add_items(self):
        try:
            pedido, n_simafic, qtd_items = self.pedido.text(), self.n_simafic.text(), self.qtd_items.text()
            print ("Add Pedido: {} {} {}".format(pedido, n_simafic, qtd_items))
            if services.validateCadastro(pedido, n_simafic, qtd_items):
                print ("Add Pedido: {} {} {}".format(pedido, n_simafic, qtd_items))
                mb = QMessageBox()
                mb.setIconPixmap(QPixmap('assets/check_icon_blue2'))
                mb.setWindowTitle("Sucesso")
                mb.setText('O pedido: {} foi criado com sucesso!'.format(pedido))
                services.add_pedido(pedido, n_simafic, qtd_items)
                mb.exec_()
                self.update_model_tableview()
                self.limpar_pedidos()
                

        except (ValidationError, DBPedidosException) as error:
            error_dialog = QErrorMessage()  
            error_dialog.setWindowTitle(error.errors)
            error_dialog.setWindowIcon(QIcon(main_icon))
            error_dialog.showMessage(error.message)
            error_dialog.exec_()
        
        pass
    
    def update_model_tableview(self):
        self.modelAllPedidos.setDataFrame(services.get_all_pedidos_df())
        self.topRightGroupBox.setCurrentIndex(0)

    def limpar_pedidos(self):
        self.n_simafic.clear()
        self.qtd_items.clear()
        self.pedido.clear()

    def goMainWindow(self):
        self.cams = mainView
        self.cams.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cadastroPedidos = CadastroPedidos()
        self.title = "Inove Confecções App"
        self.setMinimumSize(QSize(h_size, v_size))
        self.originalPalette = QApplication.palette()
        self.setWindowIcon(QtGui.QIcon(main_icon))
        self.setWindowTitle("Inove")
        self.setStyleSheet(style)
        self.InitUI()
        errorSound = QSound('assets/error.wav')
        errorSound.play()

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
        self.cadastroPedidos.show()
        self.hide()

    @pyqtSlot()
    def operacaoLogistica(self):
        self.statusBar().showMessage("Switched to OperacaoLogistica")
        self.cams = OperacaoLogistica() 
        self.cams.show()
        self.close()

class UpdateScreen(QDialog):
    def __init__(self, pedido,parent=None):
        super(UpdateScreen, self).__init__(parent, Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle('Alterar Item')
        self.setMinimumSize(QSize((h_size/2), (v_size/2)))
        self.setWindowIcon(QIcon(main_icon))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.topLeftGroupBox = QGroupBox("Alterar Pedido")

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.item = pedido
        
        formLayout = QFormLayout()

        id_ped = QLineEdit(self)
        id_ped.setText(str(self.item.id))
        id_ped.setDisabled(True)
        id_ped_label = QLabel("Id no Sistema:")

        self.pedido = QLineEdit(self)
        self.pedido.setText(self.item.id_pedido)
        pedido_label = QLabel("Pedido:")
        self.pedido.textChanged.connect(lambda x: self.item.set_id_pedido(x))
        self.pedido.setDisabled(True)

        self.n_simafic = QLineEdit(self)
        self.n_simafic.setText(self.item.cod_simafic)
        n_simafic_label = QLabel("COD. SIMAFIC:")
        self.n_simafic.textChanged.connect(lambda x: self.item.set_cod_simafic(x))
        self.n_simafic.setDisabled(True)

        self.desc = QLineEdit(self)
        self.desc.setText(self.item.desc)
        desc_label = QLabel("DESC:")
        self.desc.textChanged.connect(lambda x: self.item.set_desc(x))


        self.qtd_scan = QLineEdit(self)
        self.qtd_scan.setText(str(self.item.qty_scanneada))
        qtd_items_scan_label = QLabel("Quantidade de Scanneados:")
        self.qtd_scan.setDisabled(True)


        self.qtd_items = QLineEdit(self)
        self.qtd_items.setText(str(self.item.qty_total))
        qtd_items_label = QLabel("Quantidade de Items:")
        self.qtd_items.textChanged.connect(lambda x: self.item.set_qty_total(x))


        self.id_caixa = QLineEdit(self)
        self.id_caixa.setText(str(self.item.id_caixa))
        id_caixa_label = QLabel("Id da Caixa:")
        self.id_caixa.textChanged.connect(lambda x: self.item.set_id_caixa(x))


        self.nome_resp = QLineEdit(self)
        self.nome_resp.setText(str(self.item.nome_responsavel))
        nome_resp_label = QLabel("Nome do responsável:")
        self.nome_resp.textChanged.connect(lambda x: self.item.set_nome_responsavel(x))


        '''ADD PEDIDO'''
        add_item = QPushButton('Confirmar Alteração')
        add_item.setObjectName('Add')
        add_item.setIcon(QIcon('assets/check_icon_blue2.png'))
        add_item.clicked.connect(lambda : self.updateItens())

        '''CLEAR BUTTON CONFIG '''
        clear_btn = QPushButton('Cancelar Alteração')
        clear_btn.setObjectName('Yellow')
        clear_btn.setIcon(QIcon('assets/eraser.png'))
        clear_btn.clicked.connect(lambda : self.cancelar())

        formLayout.addRow(id_ped_label, id_ped)                
        formLayout.addRow(pedido_label, self.pedido)
        formLayout.addRow(n_simafic_label, self.n_simafic)
        formLayout.addRow(desc_label, self.desc)
        formLayout.addRow(qtd_items_scan_label, self.qtd_scan)
        formLayout.addRow(qtd_items_label, self.qtd_items)
        formLayout.addRow(id_caixa_label, self.id_caixa)
        formLayout.addRow(nome_resp_label, self.nome_resp)
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
        layout.addStretch(1)
         
        self.setLayout(layout)

    def updateItens(self):
        services.update_pedido(self.item)
        self.parent().update_model_tableview()
        self.parent().limpar_pedidos()
        self.close()
        pass
    def cancelar(self):
        self.close()
        pass

    

class OperacaoLogistica(QDialog):
    #TODO: Acertar formatação na listagem de items por SIMAFIC 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle('Operação Logística')
        self.setMinimumSize(QSize(h_size, v_size))
        self.setWindowIcon(QIcon(main_icon))

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        #Pedido Input Field
        self.proxy_list_result_id = QSortFilterProxyModel()
        self.numero_pedido = QLineEdit(self)
        self.numero_pedido.setPlaceholderText("Insira o Número do Pedido")
        self.numero_pedido.textChanged.connect(lambda wildcard: self.proxy_list_result_id.setFilterWildcard(wildcard))


        #Voltar Btn
        self.voltar_btn = QPushButton(self)
        #self.voltar_btn.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.voltar_btn.setText('Voltar')
        self.voltar_btn.clicked.connect(self.goMainWindow)
        self.close()

        #Adicionar Cores no StyleSheet
        colors = ['##393318', '  ##fff']
        self.pedidos = services.get_all_pedidos()
        self.item_result = None
        self.item_escolhido = None

        self.id_pedido_list = QListView()
        self.simafics_do_id = QListWidget()
        #self.simafics_do_id.setHidden(True)
        self.createPedidoIdList()

        self.id_pedido_list.clicked.connect(lambda id_pedido: self.createListaSimafics(id_pedido))
        self.simafics_do_id.itemDoubleClicked.connect(lambda pedido: self.simaficSelecionado(pedido))

        self.pedidos_label = QLabel()
        self.pedidos_label.setBuddy(self.id_pedido_list)
        self.simafic_label = QLabel()
        self.simafic_label.setBuddy(self.simafics_do_id)

        
        self.itensTree = PedidoItensTree()
        self.treeItensTV = QTreeView()
        self.treeItensTV.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeItensTV.setAlternatingRowColors(True)
        self.treeItensTV.setRootIsDecorated(True)
        self.treeItensTV.doubleClicked.connect(self.simaficSelecionado)
        self.treeItensTV.setColumnHidden(8, True)
        

        


        if len(self.pedidos) <= 0:
            self.pedidos_label.setText("É necessário adicionar um pedido na tela de cadastro.")
            self.pedidos_label.setStyleSheet("QLabel { color: red; }");
        else:
            self.pedidos_label.setText("Listagem de Pedidos:")
            self.pedidos_label.setStyleSheet("QLabel { color: black; }");
            self.simafic_label.setText("Selecione um pedido para ver a listagem de Itens por SIMAFIC:")
            self.simafic_label.setStyleSheet("QLabel { color: red; }");

        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.addWidget(self.numero_pedido,0,0)
        layout.addWidget(self.voltar_btn,0,1)
        layout.addWidget(self.pedidos_label, 1,0)
        layout.addWidget(self.simafic_label, 1, 1)
        layout.addWidget(self.id_pedido_list,2,0)
        layout.addWidget(self.treeItensTV, 2,1)
        #layout.addWidget(self.simafics_do_id, 2,1)
        self.setLayout(layout)

    def createPedidoIdList(self):
        print('def createPedidoIdList(self):')
        onlyids = set()
        pedidosbyid = []
        pedidosCompletos = []
        self.proxy_list_result_id = QSortFilterProxyModel()
        for obj in self.pedidos:
            if obj.id_pedido not in onlyids:
                pedidosbyid.append(obj)
                onlyids.add(obj.id_pedido)

        self.pedidoId_model = QStringListModel(onlyids, self)
        self.proxy_list_result_id.setSourceModel(self.pedidoId_model)
        self.id_pedido_list.setModel(self.proxy_list_result_id)
        self.id_pedido_list.setAlternatingRowColors(True)
        self.id_pedido_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

       

    def createListaSimafics(self, id_pedido):

        pedido = id_pedido.data()
        self.pedidosModel = self.itensTree.createPedidosModel(self.itensTree)
        self.treeItensTV.setModel(self.pedidosModel)
        print('def listaSimafics(self, id_pedido): {id_pedido}'.format(id_pedido=pedido))
        self.item_result = None
        self.item_result = [x for x in self.pedidos if x.id_pedido == pedido]
        self.simafics_do_id.clear()
        self.pedidosModel.beginResetModel
        self.pedidosModel.modelReset
        self.pedidosModel.endResetModel
    
        for idx, item in enumerate(self.item_result):
            print(item)
            self.itensTree.addItens(self.pedidosModel, item.cod_simafic, item.desc, item.qty_scanneada, item.qty_total, item.nome_responsavel, item.id_caixa, item.time_updated.strftime("%d/%m/%y %H:%M:%S"), item.id_pedido, item)

        self.simafic_label.setText("Listagem de Itens do pedido {} por SIMAFIC:".format(pedido))
        self.simafic_label.setStyleSheet("QLabel { color: black; }")

        
        #self.simafics_do_id.setHidden(False)
        

    def simaficSelecionado(self, item):
        print(item.column(), item.row())
        simafic_escolhido = self.treeItensTV.model().index(item.row(), 0).data()
        id_pedido = self.treeItensTV.model().index(item.row(), 7).data()
        self.item_escolhido = [x for x in self.item_result if x.cod_simafic == simafic_escolhido and x.id_pedido == id_pedido]
        self.cams = ItemScanner(self.item_escolhido[0])
        self.cams.show()
        self.close()

    def goMainWindow(self):
        self.cams = mainView
        self.cams.show()
        self.close()

    def goScan(self):
        self.cams = ItemScanner("Eu sou o Pedido", "Eu sou o Simafic", "Eu sou a Descrição", "300")
        self.cams.show()
        self.close()


class ItemScanner(QDialog):
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        
        self.pedido = item
        self.font = QFont()
        self.fontScan = QFont()
        self.fontScan.setPointSize(14)
        self.font.setPointSize(16)
        self.setStyleSheet('assets/style.py')
        self.setWindowTitle('Scanner')
        self.setWindowIcon(QIcon(main_icon))
        self.setMinimumSize(QSize(h_size, v_size))
        voltar_btn = QPushButton('Voltar')
        voltar_btn.clicked.connect(self.goOperacoesLogisticas)
        voltar_btn.setFocusPolicy(Qt.NoFocus)
        
        titleLabel = QLabel('Pedido Nº {pedido}'.format(pedido=self.pedido.id_pedido))
        titleLabel.setFont(self.font)        
        titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setObjectName('ScanTitle')


        vLayout= QVBoxLayout()
        self.createPedidoInfo()
        self.createCountElement()
        
        self.validaQuantidade()

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

    def validaQuantidade(self):
        if services.validaQtdPedido(self.pedido):
            pass;
        else:
            self.pedidoInfoBox.setDisabled(True)
            self.countElementGroupBox.setDisabled(True)

    def createPedidoInfo(self):
        self.pedidoInfoBox = QGroupBox()
        finalInfoLayout = QVBoxLayout()
        scanInfoLayout = QFormLayout()

        self.count_resp_le = QLineEdit(self)
        self.count_resp_le.setPlaceholderText("ex. John Doe")
        if (self.pedido.nome_responsavel not in "A ser definido."):
            self.count_resp_le.setText(self.pedido.nome_responsavel)
            self.count_resp_le.setDisabled(True)


        self.id_caixa_le = QLineEdit(self)
        self.id_caixa_le.setPlaceholderText("ex. 12AB")
        if (self.pedido.id_caixa not in "A ser definido."):
            self.id_caixa_le.setReadOnly(True)
            self.id_caixa_le.setText(self.pedido.id_caixa)

        desc_le = QLineEdit(self.pedido.desc)
        desc_le.setText = self.pedido.desc
        desc_le.setReadOnly(True)
        desc_le.setDisabled(True)

        simafic_le = QLineEdit(self.pedido.cod_simafic)
        simafic_le.setText = self.pedido.cod_simafic
        simafic_le.setReadOnly(True)
        simafic_le.setDisabled(True)

        #scanLayout.addWidget(self.voltar_btn)
        scanInfoLayout.addRow("Descrição:", desc_le)
        scanInfoLayout.addRow("COD. SIMAFIC:", simafic_le)
        scanInfoLayout.addRow("Responsável pela contagem:", self.count_resp_le)
        scanInfoLayout.addRow("Numero da Caixa:", self.id_caixa_le)
        scanInfoLayout.setContentsMargins(75,75,75,10)

        buttonsLayout = QHBoxLayout()

        self.startCount = QPushButton('Confirmar')
        self.startCount.clicked.connect(self.validaPedidoInfo)

        cancelarCount = QPushButton('Cancelar')
        cancelarCount.clicked.connect(self.cancelarScan)
        cancelarCount.setFocusPolicy(Qt.NoFocus)

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

        self.qtd_parcial_le = QLineEdit()
        qtd_total_le = QLineEdit()
        qtd_total_le.setFont(self.font)
        self.qtd_parcial_le.setFont(self.font)
        self.qtd_parcial_le.setText(str(self.pedido.qty_scanneada))
        self.qtd_parcial_le.setReadOnly(True)
        qtd_total_le.setText(str(self.pedido.qty_total))
        qtd_total_le.setReadOnly(True)

        qtd_parcial_label.setBuddy(self.qtd_parcial_le)
        qtd_total_label.setBuddy(self.qtd_parcial_le)

        input_scan_label = QLabel('Scanneie o COD. SIMAFIC do Produto:')
        input_scan_label.setFont(self.fontScan)
        input_scan_label.setAlignment(Qt.AlignCenter)
        self.input_scanner = QLineEdit()
        self.input_scanner.setAlignment(Qt.AlignCenter)
        self.input_scanner.setFont(self.fontScan)
        self.input_scanner.returnPressed.connect(self.validaScanInput)
        input_scan_label.setBuddy(self.input_scanner)

        hCountLayout.addStretch(1)
        hCountLayout.addWidget(qtd_parcial_label)
        hCountLayout.addWidget(self.qtd_parcial_le)
        hCountLayout.addStretch(1)
        hCountLayout.addWidget(qtd_total_label)
        hCountLayout.addWidget(qtd_total_le)
        hCountLayout.addStretch(1)
        hCountLayout.setContentsMargins(0,30,0,0)
        scanLayout.setContentsMargins(75,20,75,75)

    
        scanLayout.addWidget(input_scan_label)
        scanLayout.addWidget(self.input_scanner)
        scanLayout.addStretch(1)
        scanLayout.addLayout(hCountLayout)
        scanLayout.addStretch(3)

        self.countElementGroupBox.setLayout(scanLayout)
        self.countElementGroupBox.setDisabled(True)

    
    def validaPedidoInfo(self):
        try:
            print ("validateInfoScan")
            services.validateInfoScan(self.count_resp_le.text(), self.id_caixa_le.text(), self.pedido)
            self.startCount.setDisabled(True)
            self.count_resp_le.setDisabled(True)
            self.id_caixa_le.setDisabled(True)
            self.countElementGroupBox.setDisabled(False)
            self.input_scanner.setFocus()
        
        except (ValidationError, DBPedidosException) as error:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle(error.errors)
            error_dialog.setWindowIcon(QIcon(main_icon))
            error_dialog.showMessage(error.message)
            error_dialog.exec_()
       
        
    def cancelarScan(self):
        buttonReply = QMessageBox.question(self, 'Cancelamento de Contagem', "Deseja cancelar a contagem? Os itens contados serão desconsiderados.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Cancelamento de pedido aprovado por {}.'.format(self.count_resp_le.text()))
            services.update_cancelar_scan(self.pedido)
            self.goOperacoesLogisticas()
        else:
           pass;
        
    def validaScanInput(self):
        print('validaScanInput {}'.format(self.input_scanner.text()))
        try:
            if services.valida_simafic(s_input=self.input_scanner.text(), pedido=self.pedido):
                self.pedido.qty_scanneada += 1
                self.qtd_parcial_le.setText(str(self.pedido.qty_scanneada))
                self.pedido.nome_responsavel = self.count_resp_le.text()
                self.pedido.id_caixa = self.id_caixa_le.text()
                services.update_pedido(self.pedido)
                self.input_scanner.clear()
                if (self.pedido.qty_scanneada == self.pedido.qty_total):
                    print ("Aqui é pra tocar o som")
                    QSound.play('assets/error.wav')
                    self.input_scanner.setDisabled(True)
                    QMessageBox.warning(
                        self, "Item finalizado.",
                        "O Item já atingiu a quantidade cadastrada."
                    )
        except (ValidationError, DBPedidosException) as error:
            error_dialog = QErrorMessage()
            errorSound = QSound('assets/error.wav')
            errorSound.play()
            error_dialog.setWindowTitle(error.errors)
            error_dialog.setWindowIcon(QIcon(main_icon))
            error_dialog.showMessage(error.message)
            self.input_scanner.clear()
            error_dialog.exec_()
        
        


    def goOperacoesLogisticas(self):
        self.cams = OperacaoLogistica()
        self.cams.show()
        self.close()

    def goMainWindow(self):
        self.cams = mainView
        self.cams.show()
        self.close() 

if __name__ == '__main__':

    import sys
    main_icon = str(services.get_main_icon())
    h_size=int(services.get_h_size())
    v_size=int(services.get_v_size())
    style = getStyle()
    pp = pprint.PrettyPrinter(indent=4)
    app = QApplication(sys.argv)
    mainView = MainWindow()
    #mainView.clearFocus()
    mainView.show()
    
    #gallery.show()
    #gallery.show()
    sys.exit(app.exec_())

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
