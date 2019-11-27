import os
import random as rnd
import pandas as pd
import classes.pedidodao as pdao
from pandas import ExcelWriter
from pandas import ExcelFile


def comparator():
    # pedido = input("INSIRA O NUMERO DO PEDIDO: ")
    # produto = input("INSIRA O CÓDIGO SIMAFIC DO PRODUTO: ")
    # npedido = input("NUMERO DE ITENS DO PRODUTO: ")

    pedido = '123'
    produto = '08.04.02.507-6'
    npedido = 10
    
    result = validadorProduto(produto)

    pedido = pdao.Pedido(id_pedido=pedido, id_product=result.get(0), desc=result.get(1), qty_total=int(npedido), qty_scanneada=0)
    pdao.inserirPedido(pedido)
    pedidoselecionado = pdao.queryAllPedidos()
    print (pedidoselecionado)
    # print (result)

def validadorProduto(produto):
    df = pd.read_excel('plan_test.xlsx', index_col=None, header=None)
    roupa_dict = df.T.to_dict().values()
    for val in roupa_dict:
        print (val.get(0))
        if (produto == val.get(0)):
            print("O SEU PRODUTO EXISTE! PARABÉNS: {}".format(val.get(0)))
            print(val.get(1))
            return val

def getValidFormat():
    df = pd.read_excel('plan_test.xlsx', index_col=None, header=None)
    return df    

#def validadorCampos()


comparator()
