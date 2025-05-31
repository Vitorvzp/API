from sqlmodel import SQLModel, Field, create_engine
from time import sleep as s
from os import path as p


class Usuario(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    idade: int
    cpf: str
    gmail: str
    ano: int

# Nome, Salário, Saldo ,CPF, Usuário e senha
class Funcionarios(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    salario: float
    saldo: float
    cpf: str
    usuario: int
    senha: str

# Nome, Preço e Quantidade
class Produtos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    preco: float
    quantidade: str

connection_string = f"sqlite:///Data/database.db"

engine = create_engine(connection_string)

SQLModel.metadata.create_all(engine)
