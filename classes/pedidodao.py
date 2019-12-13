
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exemplo de CRUD com SQLAlchemy e SQLite3"""

import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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

    id = Column(Integer, primary_key=True, nullable=False)
    id_pedido = Column(String(80), unique=False, nullable=False)
    id_product = Column(String(80), unique=False, nullable=False)
    desc = Column(String(80), unique=False, nullable=False)
    qty_total = Column(Integer, unique=False, nullable=False)
    qty_total = Column(Integer, unique=False, nullable=False)

    def __init__(self, id_pedido, id_product, desc, qty_total, qty_scanneada):
        """Construtor.
        Utilizando o construtor para passar os valores
        no momento em que a classe é instanciada.
        :param nome: (str).
        :param idade: (int).
        :param sexo: (str).
        """
        self.id_pedido = int(id_pedido)
        self.id_product = str(id_product)
        self.desc = str(desc)
        self.qty_total = int(qty_total)
        self.qty_scanneada = int(qty_scanneada)

    def __repr__(self):
        return "<{klass} @{id:x} {attrs}>".format(
            klass=self.__class__.__name__,
            id=id(self) & 0xFFFFFF,
            attrs=" ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
            )
            
    def asdict(self):
        return {'Pedido': self.id_pedido, 'Produto': self.id_product, 'desc': self.desc}

if __name__ == "__main__":
    # Removendo todas as tabelas do banco.
    # Base.metadata.drop_all(engine)

    # Criando todas as tabelas.
    Base.metadata.create_all(engine)

    # Criando uma sessão (add, commit, query, etc).
    session = Session()

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
    session.close()
#!/usr/bin/env python
else :

    def inserirPedido(pedido):
        session = Session()
        session.add(pedido)
        session.commit()
        session.close()

    def queryAllPedidos():
        session = Session()
        dados = session.query(Pedido).all()
        session.close()
        return dados

    def dinamicQuery(id_pedido):
        session = Session()
        print (str(id_pedido))
        dados = session.query(Pedido).filter_by(id_pedido = id_pedido).all()

        session.close()
        return dados
