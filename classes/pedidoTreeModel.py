#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
QWidget)

class PedidoItensTree(QWidget):
    
    cod_simafic, desc, qty_scanneada, qty_total, nome_responsavel, id_caixa, time_updated, id_pedido = range(8)
    
    def __init__(self):
        super().__init__()

    def createPedidosModel(self,parent):
        model = QStandardItemModel(0, 8, parent)
        model.setHeaderData(self.cod_simafic, Qt.Horizontal,"COD. SIMAFIC")
        model.setHeaderData(self.qty_scanneada, Qt.Horizontal, "Qtd. Atual")
        model.setHeaderData(self.qty_total, Qt.Horizontal, "Qtd. Total")
        model.setHeaderData(self.nome_responsavel, Qt.Horizontal, "Responsável")
        model.setHeaderData(self.id_caixa, Qt.Horizontal, "Nº da Caixa")
        model.setHeaderData(self.time_updated, Qt.Horizontal, "Data de Atualização")
        model.setHeaderData(self.desc, Qt.Horizontal, "Descrição")
        model.setHeaderData(self.id_pedido, Qt.Horizontal, "Nº Pedido")
        
        return model
    
    def addItens(self,model, cod_simafic, desc, qty_scanneada, qty_total, nome_responsavel, id_caixa, time_updated, id_pedido, item):
        model.insertRow(0)
        model.setData(model.index(0, self.cod_simafic), cod_simafic)
        model.setData(model.index(0, self.desc), desc)
        model.setData(model.index(0, self.qty_scanneada), qty_scanneada)
        model.setData(model.index(0, self.qty_total), qty_total)
        model.setData(model.index(0, self.nome_responsavel), nome_responsavel)
        model.setData(model.index(0, self.id_caixa), id_caixa)
        model.setData(model.index(0, self.time_updated), time_updated)
        model.setData(model.index(0, self.id_pedido), id_pedido)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PedidoItensTree()
    sys.exit(app.exec_())