import os
import random as rnd
import pandas as pd
import classes.pedidodao as pdao
from classes.dfmodel import DataFrameModel as PandasModel
import json
from pandas import ExcelWriter
from pandas import ExcelFile
from property_reader import getConfig


def comparator():

    pedido = '123'
    produto = '08.04.02.499-9'
    npedido = 10
    
    result = validaItem(produto)

    pedido = pdao.Pedido(id_pedido=pedido, id_product=result.get('CODIGO'), desc=result.get('DESCRICAO'), qty_total=int(npedido), qty_scanneada=0)
    pdao.inserirPedido(pedido)
    pedidoselecionado = pdao.queryAllPedidos()
    print (pedidoselecionado)
    # print (result)

def validaItem(produto):
    roupa_dict = df.T.to_dict().values()
    for val in roupa_dict:
        print (val)
        if (produto in val.get('CODIGO')):
            print("Produto encontrado: ".format(val.get('CODIGO')))
            print(val.get('CODIGO'))
            return val

def get_simafic_as_dataframe():
    validDf = loadValidXLS()
    #validDf = validDf.sort_values(by='TAMANHO')
    model = PandasModel(validDf)
    return model

def loadRawXLS():
    roupa_dict = df.T.to_dict().values()
    for val in roupa_dict:
        #print (val.get(0))
        val.update({'TAMANHO': str(val['DESCRICAO']).rsplit(' ', 1)[-1]})
    return pd.DataFrame.from_dict(roupa_dict)

def loadValidXLS():
    roupa_dict = df.T.to_dict().values()
    resultList = list()
    for val in roupa_dict:
        #print (val.get(0))
        sample = str(val['DESCRICAO']).rsplit(' ', 1)[-1]
        if sample in valoresPermitidos:
            val.update({'TAMANHO': sample })
            resultList.append(val)

    resultdf = pd.DataFrame.from_dict(resultList)
    resultdf.reindex(index=range(1,len(resultList)))
    return pd.DataFrame.from_dict(resultList)

def get_all_pedidos():
    arr = pdao.queryAllPedidos()
    print(arr)
    variables = pdao.Pedido.__dict__.keys()
    print (variables)
    df = pd.DataFrame([[getattr(i,j) for j in variables] for i in arr], columns = variables)
    return PandasModel(df)

def get_main_icon():
    return getConfig('inova', 'icon')

def get_h_size():
    return getConfig('inova', 'h_size')

def get_v_size():
    return getConfig('inova', 'v_size')

if __name__ == "__main__":
    df = pd.read_excel('plan_test.xlsx', index_col=None, header=0)
    valoresPermitidos = json.loads(getConfig('filtros', 'tamanhos'))
    print(loadValidXLS())
    #get_simafic_as_dataframe()
    comparator()
else:
    df = pd.read_excel('plan_test.xlsx', index_col=None, header=0)
    valoresPermitidos = json.loads(getConfig('filtros', 'tamanhos'))

    #comparator()
