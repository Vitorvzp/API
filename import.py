from os import path as p
import Functions.database
from sqlmodel import Session, select
from threading import Thread
import Functions.security

criptografar = Functions.security.criptografar
engine = Functions.database.engine
Usuario = Functions.database.Usuario
Funcionarios = Functions.database.Funcionarios
Produtos = Functions.database.Produtos


paths = ["Usuarios.txt","Funcionarios.txt","Produtos.txt","Usuarios2.txt","Usuarios3.txt"]
def users():
  with Session(engine) as session:
    with open(p.join("Imports", paths[0]), "r", encoding='utf-8') as ler:
      lines = ler.readlines()
      x = 0
      for line in lines:
        x+=1
        line = line.split(',')
        nome = line[0].strip()
        idade = line[1].strip()
        cpf = line[2].strip()
        gmail = line[3].strip()
        ano = line[4].strip()
        nome = criptografar(nome)
        cpf = criptografar(cpf)
        gmail = criptografar(gmail)
        usuario = Usuario(nome=nome, idade=idade, cpf=cpf, gmail=gmail, ano=ano)
        session.add(usuario)
        if x == 99999:
          session.commit()
        if x == 199999:
          session.commit()
        if x == 299999:
          session.commit()
      session.commit()
def users2():
  with Session(engine) as session:
    with open(p.join("Imports", paths[3]), "r", encoding='utf-8') as ler:
      lines = ler.readlines()
      x = 0
      for line in lines:
        x+=1
        line = line.split(',')
        nome = line[0].strip()
        idade = line[1].strip()
        cpf = line[2].strip()
        gmail = line[3].strip()
        ano = line[4].strip()
        nome = criptografar(nome)
        cpf = criptografar(cpf)
        gmail = criptografar(gmail)
        usuario = Usuario(nome=nome, idade=idade, cpf=cpf, gmail=gmail, ano=ano)
        session.add(usuario)
        if x == 99999:
          session.commit()
        if x == 199999:
          session.commit()
        if x == 299999:
          session.commit()
      session.commit()
def users3():
  with Session(engine) as session:
    with open(p.join("Imports", paths[4]), "r", encoding='utf-8') as ler:
      lines = ler.readlines()
      x = 0
      for line in lines:
        x+=1
        line = line.split(',')
        nome = line[0].strip()
        idade = line[1].strip()
        cpf = line[2].strip()
        gmail = line[3].strip()
        ano = line[4].strip()
        nome = criptografar(nome)
        cpf = criptografar(cpf)
        gmail = criptografar(gmail)
        usuario = Usuario(nome=nome, idade=idade, cpf=cpf, gmail=gmail, ano=ano)
        session.add(usuario)
        if x == 99999:
          session.commit()
        if x == 199999:
          session.commit()
        if x == 299999:
          session.commit()
      session.commit()

def funcs():
  with Session(engine) as session:
    with open(p.join("Imports", paths[1]), "r", encoding='utf-8') as ler:
      lines = ler.readlines()
      x = 0
      for line in lines:
        x+=1
        line = line.split(',')
        nome = line[0].strip()
        salario = line[1].strip()
        saldo = line[2].strip()
        cpf = line[3].strip()
        usuario = line[4].strip()
        senha = line[5].strip()
        nome = criptografar(nome)
        cpf = criptografar(cpf)
        usuario = criptografar(usuario)
        senha = criptografar(senha)
        funcionarios = Funcionarios(nome=nome, salario=salario, saldo=saldo, cpf=cpf, usuario=usuario, senha=senha)
        session.add(funcionarios)
      session.commit()

def products():
  with Session(engine) as session:
    with open(p.join("Imports", paths[2]), "r", encoding='utf-8') as ler:
      lines = ler.readlines()
      x = 0
      for line in lines:
        x+=1
        line = line.split(',')
        nome = line[0].strip()
        preco = line[1].strip()
        quantidade = line[2].strip()
        nome = criptografar(nome)
        produtos = Produtos(nome=nome, preco=preco, quantidade=quantidade)
        session.add(produtos)
      session.commit()

if __name__ == "__main__":
  users()
  funcs()
  products()