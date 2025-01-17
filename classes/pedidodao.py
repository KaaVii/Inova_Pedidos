
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exemplo de CRUD com SQLAlchemy e SQLite3"""

from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, create_engine, DateTime, event, DDL, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Sequence
import os

from datetime import datetime, timedelta


# Criar banco na memória
# engine = create_engine('sqlite://')

# Caminho relativo (pode ser utilizado o caminho absoluto):
engine = create_engine('sqlite:///db.sqlite3')

# Para utilizar o debug utilizar deve-se adicionar ``echo=True``:
# engine = create_engine('sqlite:///db.sqlite3', echo=True)

# Criando uma classe "Session" já configurada.
# Session é instanciado posteriormente para interação com a tabela.
Session = sessionmaker(bind=engine)

Base = declarative_base()



class Pedido(Base):
    """Cada classe representa uma tabela do banco"""
    # Nome da tabela, se a variável não for
    # declarada será utilizado o nome da classe.
    __tablename__ = 'Pedido'
    __table_args__ = {'sqlite_autoincrement': True}

    id=Column('id', Integer)
    id_pedido = Column(String(80), unique=False, nullable=False, primary_key=True)
    cod_simafic = Column(String(80), unique=False, nullable=False, primary_key=True)
    desc = Column(String(200), unique=False, nullable=False)
    qty_scanneada = Column(Integer, unique=False, nullable=False)
    qty_total = Column(Integer, unique=False, nullable=False)
    nome_responsavel = Column(String(120), unique=False, nullable=False, default="Pedido ainda não possui responsável atribuído.")
    id_caixa = Column(String(80), unique=False, nullable=False, default="Pedido ainda não possui caixa atribuída.")
    data_criacao = Column(DateTime, default=datetime.now)
    time_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __init__(self, id_pedido, cod_simafic, desc, qty_total, qty_scanneada, nome_responsavel, id_caixa):
       
        self.id_pedido = id_pedido
        self.cod_simafic = str(cod_simafic)
        self.desc = str(desc)
        self.qty_total = int(qty_total)
        self.qty_scanneada = int(qty_scanneada)
        self.nome_responsavel = str(nome_responsavel)
        self.id_caixa = str(id_caixa)

    def __repr__(self):
        return "<{klass} @{id:x} {attrs}>".format(
            klass=self.__class__.__name__,
            id=id(self) & 0xFFFFFF,
            attrs=" ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
            )
            
    def asdict(self):
        return ({'Pedido': self.id_pedido, 'COD. SIMAFIC': self.cod_simafic, 
        'Descrição': self.desc, 'Qtd. Total': self.qty_total, 
        'Qtd. Scanneada': self.qty_scanneada, 'Nº da Caixa':self.id_caixa, 
        'Responsável': self.nome_responsavel,'Data Criação': self.data_criacao.strftime("%d/%m/%y %H:%M:%S"),
        'Data Atualização':self.time_updated.strftime("%d/%m/%y %H:%M:%S")})

    def set_id_pedido(self, a): 
        print("set_id_pedido method called") 
        self.id_pedido = str(a) 
    def set_cod_simafic(self, a): 
        print("set_cod_simafic method called") 
        self.cod_simafic = str(a) 
    def set_desc(self, a): 
        print("set_desc method called") 
        self.desc = str(a) 
    def set_qty_total(self, a): 
        print("set_qty_total method called") 
        self.qty_total = int(a) 
    def set_nome_responsavel(self, a): 
        print("set_nome_responsavel method called") 
        self.nome_responsavel = str(a)
    def set_id_caixa(self, a): 
         print("set_id_caixa method called") 
         self.id_caixa = str(a)

if __name__ == "__main__":
    # Removendo todas as tabelas do banco.
    # Base.metadata.drop_all(engine)

    def createDb():
        # Criando todas as tabelas.
        Base.metadata.create_all(engine)

    # Criando uma sessão (add, commit, query, etc).
        session = Session()
        session.close()
    createDb()

    # Criando os dados que serão inseridos na tabela.
    # Classe com o construtor.
    # usuario = NomeDaTabela('Felipe', 35, 'Masculino')
    # usuarios = [NomeDaTabela('Maria', 20, 'Feminino'), NomeDaTabela('Pedro', 50, 'Masculino')]

    # Caso não seja utilizado o construtor na classe
    # os dados são passados depois de se criar a instancia.
    # usuario = NomeDaTabela()
    # usuario.nome = 'Camila'
    # usuario.idade = 50
    # usuario.sexo = 'Feminino'

    # Inserindo registro na tabela.
    # session.add(usuario)

    # Inserindo vários registros na tabela.
    # session.add_all(usuarios)

    # Persistindo os dados.
    # session.commit()

    # Consultar todos os registros.
    # dados = session.query(NomeDaTabela).all()
    # print(dados)
    # for linha in dados:
    #     print(f'Nome: {linha.nome} - Idade: {linha.idade} - Sexo: {linha.sexo}')

    # Consulta registros com filtro.
    # dados = session.query(NomeDaTabela).filter(NomeDaTabela.idade > 40).all()
    # print(dados)
    # for linha in dados:
    #     print(f'Nome: {linha.nome} - Idade: {linha.idade} - Sexo: {linha.sexo}')

    # Alterar um registro da tabela.
    # print('Nome ANTES da alteração:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one().nome)
    # session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).update({'nome': 'Roberto'})
    # session.commit()
    # print('Nome DEPOIS da alteração:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one().nome)

    # Remover um registro da tabela.
    # print('Registro ANTES da remoção:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one_or_none())
    # session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).delete()
    # session.commit()
    # print('Registro DEPOIS da remoção:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one_or_none())

    # Fechando a sessão.
        
#!/usr/bin/env python
else :

    if not (os.path.isfile('../db.sqlite3') or os.path.isfile('db.sqlite3')):
        print('sqlite não encontrado, criando banco...')
        createDb()

    def inserirPedido(pedido):
        pedido.id = id(pedido)
        session = Session()
        session.add(pedido)
        session.commit()
        session.close()

    def queryAllPedidos():
        
        session = Session()
        dados = session.query(Pedido).all()
        session.close()
        return dados
  
    def update_pedido(pedido):
        session = Session() 
        pedido.time_update = datetime.now
        session.query(Pedido).filter_by(id_pedido=pedido.id_pedido).filter_by(cod_simafic=pedido.cod_simafic).update({column: getattr(pedido, column) for column in Pedido.__table__.columns.keys()})
        session.commit()
        #session.query(Pedido).filter(Pedido.id_pedido == pedido.id_pedido).one().id_pedido
            
    def dinamicQuery(id_pedido):
        session = Session()
        print (str(id_pedido))
        dados = session.query(Pedido).filter_by(id_pedido = id_pedido).all()

        session.close()
        return dados

    def dinamicQueryItem(id_pedido, simafic):
        session = Session()
        print (str(id_pedido))
        dados = session.query(Pedido).filter_by(id_pedido = id_pedido).filter_by(cod_simafic=simafic).one()

        session.close()
        return dados

    def excluirPedidoItem(pedido):
        #Remover um registro da tabela.
        session = Session()
        session.query(Pedido).filter(Pedido.id == pedido.id).delete()
        session.commit()
        print("Pedido {} Removido com Sucesso.".format(pedido))