import os
import random as rnd
import pandas as pd
import classes.pedidodao as pdao
from classes.dfmodel import DataFrameModel as PandasModel
from exceptions import ValidationError, DBPedidosException
import json
from pandas import ExcelWriter
from pandas import ExcelFile
from property_reader import getConfig
import re

patternSimafic = re.compile('[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.[0-9]{3}-[0-9]{1}')
patternPedido = re.compile('[0-9]{3}\.[0-9]{3}')

def validateCadastro(pedido, n_simafic, qtd_items):
    success = True
    error="Dados Incorretos!"
    if not(len(pedido) <= 7 and patternPedido.match(pedido)):
        success=False
        raise ValidationError("O pedido só pode conter números e no máximo 10 digitos!", error)
        pass
    if not(patternSimafic.match(n_simafic)):
        raise ValidationError("Código SIMAFIC [{}] está fora do formato padrão!".format(n_simafic), error)
        success=False
        pass
    if not(len(qtd_items) < 10 and qtd_items.isdigit()):
        raise ValidationError("O campo quantidade só pode contar numeros e no máximo 10 digitos.", error)
        success=False
        pass
    if(not validaSimaficXLS(n_simafic)):
        raise ValidationError("Código SIMAFIC não encontrado na planilha.","Simafic Incorreto!")
        success=False
        pass
    return success

def validateInfoScan(responsavel, caixa,pedido):
    success = True
    error="Dados Incorretos!"
    if not(responsavel):
        success=False
        raise ValidationError("O Campo [Responsável pela contagem] deve ser preenchido.", error)
    if not caixa:
        success=False
        raise ValidationError("O Campo [Numero da Caixa] deve ser preenchido.", error)
    return success

def valida_simafic(s_input, pedido):
    success = True
    error = "Simafic Incorreto!"
    if not(patternSimafic.match(s_input)):
        success=False
        raise ValidationError("Código SIMAFIC [{}] está fora do formato padrão!".format(s_input), error)
    if (pedido.qty_scanneada >= pedido.qty_total):
        success=False
        raise ValidationError("O Pedido já atingiu a quantidade cadastrada.", error)
    if (s_input != pedido.cod_simafic):
        success=False
        raise ValidationError("A leitura do código da embalagem [{}] não corresponde ao código [{}]. Verifique a etiqueta.".format(s_input, pedido.cod_simafic), error)
    if (s_input is pedido.cod_simafic):        
        success = True
    return success

def validaQtdPedido(pedido):
    success = True
    if (pedido.qty_scanneada >= pedido.qty_total):
        success=False
    print('validaQtdPedido | {}'.format(str(success)))
    return success

def validaSimaficXLS(n_simafic):
    roupa_dict = df.T.to_dict().values()
    success = False
    for val in roupa_dict:
        if n_simafic in val.get('CODIGO'):success= True
    return success

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

def add_pedido(pedido, n_simafic, qtd_items):
    print('Add Pedido')
    desc = df.loc[df['CODIGO'] == n_simafic, 'DESCRICAO']
    desc = desc.to_string()
    pedidoModel = pdao.Pedido(pedido, n_simafic, desc, qtd_items, 0, "A ser definido.", "A ser definido.")
    #print('pedidoModel como Dict:' ,pedidoModel)
    try:
        pdao.inserirPedido(pedidoModel)
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            raise DBPedidosException('Código SIMAFIC: {n_simafic}, já existente para este pedido de número: {pedido}.'.format(n_simafic=n_simafic,pedido=pedido),'Erro ao acessar o Banco de Dados:')
        else:
            raise DBPedidosException(str(e),'Erro ao acessar o Banco de Dados:')
def update_pedido(pedido):
    try:
        pdao.update_pedido(pedido)
    except Exception as e:
        raise DBPedidosException(str(e),'Erro ao acessar o Banco de Dados:')

def update_cancelar_scan(pedido):
    pedido.qty_scanneada=0
    try:
        pdao.update_pedido(pedido)
    except Exception as e:
        raise DBPedidosException(str(e),'Erro ao acessar o Banco de Dados:')

def get_all_pedidos_pandas():
    
    try:
        arr = pdao.queryAllPedidos()
    except Exception as e:
        raise DBPedidosException(str(e),'Erro ao acessar o Banco de Dados:')
    #print(arr)
    df = pd.DataFrame.from_records(s.asdict() for s in arr)
    #print(df)
    return PandasModel(df)

def get_all_pedidos():
    
    try:
        arr = pdao.queryAllPedidos()
    except Exception as e:
        raise DBPedidosException(str(e),'Erro ao acessar o Banco de Dados:')    
    return arr

def get_all_pedidos_df():
    try:
        arr = pdao.queryAllPedidos()
    except Exception as e:
        raise DBPedidosException(str(e),'Erro ao acessar o Banco de Dados:')
    df = pd.DataFrame.from_records(s.asdict() for s in arr)
    return df

def get_all_items_do_pedido(pedido):
    try:
        result = pdao.dinamicQuery(pedido)
    except Exception as e: 
        raise DBPedidosException(str(e), 'Erro ao acessar o Banco de Dados:')
    return result

def get_pedido_x_item(pedido, simafic):
    try:
        result = pdao.dinamicQueryItem(pedido, simafic)
    except Exception as e: 
        raise DBPedidosException(str(e), 'Erro ao acessar o Banco de Dados:')
    return result

def excluirPedidoItem(pedido):
    try:
        result = pdao.excluirPedidoItem(pedido)
    except Exception as e: 
        raise DBPedidosException(str(e), 'Erro ao acessar o Banco de Dados:')
    return result

def get_main_icon():
    return getConfig('inove', 'icon')

def get_h_size():
    return getConfig('inove', 'h_size')

def get_v_size():
    return getConfig('inove', 'v_size')

if __name__ == "__main__":
    df = pd.read_excel('plan_test.xlsx', index_col=None, header=0)
    valoresPermitidos = json.loads(getConfig('filtros', 'tamanhos'))
    validaSimaficXLS("08.05.31.404-4")

else:
    df = pd.read_excel('plan_test.xlsx', index_col=None, header=0)
    valoresPermitidos = json.loads(getConfig('filtros', 'tamanhos'))

    #comparator()
        