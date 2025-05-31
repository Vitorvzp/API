from flask import Flask, jsonify, session, render_template, request
import Functions.database
from sqlmodel import Session, null, select
import Functions.bot
from threading import Thread
from datetime import datetime

def get_ip():
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        ip = request.remote_addr
    with open('Logs/logEnters.txt', 'r', encoding='utf-8') as ler:
      ler = ler.read()
      with open('Logs/logEnters.txt', 'w', encoding='utf-8') as escrever:
        escrever.write(f'{ler}\n{datetime.now()} IP:{ip}')
    return ip

class Site():
  def __init__(self, bot):
    super(Site, self).__init__()

    self.app = Flask(__name__)

    @self.app.route('/')
    def Home():
      ip = get_ip()
      bot.send(ip)
      return render_template('index.html')

    @self.app.route('/Usuarios', methods=['GET'])
    def Usuarios():
      with Session(Functions.database.engine) as session:
        statement = select(Functions.database.Usuario)
        usuarios = session.exec(statement).all()
        with open('Logs/logUsuarios.txt', 'w', encoding='utf-8') as arquivo:
          for usuario in usuarios:
            arquivo.write(f'{usuario.id},{usuario.nome},{usuario.idade},{usuario.gmail}')
        with open('Logs/logUsuarios.txt', 'r', encoding='utf-8') as arquivo:
          return jsonify(arquivo.read())
    @self.app.route('/Usuarios/<int:id>', methods=['GET'])
    def Search_Usuarios(id):
      with Session(Functions.database.engine) as session:
        statement = select(Functions.database.Usuario).where(Functions.database.Usuario.id==id)
        usuario = session.exec(statement).first()
      return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "idade": usuario.idade,
        "cpf": usuario.cpf,
        "gmail": usuario.gmail,
        "ano": usuario.ano,
      })
    @self.app.route('/Funcionarios', methods=['GET'])
    def Funcionarios():
      with Session(Functions.database.engine) as session:
        statement = select(Functions.database.Usuario)
        usuarios = session.exec(statement).all()
        with open('Logs/logFuncionarios.txt', 'w', encoding='utf-8') as arquivo:
          for usuario in usuarios:
            arquivo.write(f'{usuario.id},{usuario.nome},{usuario.idade},{usuario.gmail}')
        with open('Logs/logFuncionarios.txt', 'r', encoding='utf-8') as arquivo:
          return jsonify(arquivo.read())
    @self.app.route('/Funcionarios/<int:id>', methods=['GET'])
    def Search_Funcionarios(id):
      with Session(Functions.database.engine) as session:
        statement = select(Functions.database.Funcionarios).where(Functions.database.Funcionarios.id==id)
        usuario = session.exec(statement).first()
      return jsonify ({
        "id": usuario.id,
        "nome": usuario.nome,
        "salário": usuario.salario,
        "saldo": usuario.saldo,
        "cpf": usuario.cpf,
        "usuario": usuario.usuario,
        "senha": usuario.senha,
      })

    @self.app.route('/Produtos', methods=['GET'])
    def Produtos():
      with Session(Functions.database.engine) as session:
        statement = select(Functions.database.Usuario)
        usuarios = session.exec(statement).all()
        with open('Logs/logProdutos.txt', 'w', encoding='utf-8') as arquivo:
          for usuario in usuarios:
            arquivo.write(f'{usuario.id},{usuario.nome},{usuario.idade},{usuario.gmail}')
        with open('Logs/logProdutos.txt', 'r', encoding='utf-8') as arquivo:
          return jsonify(arquivo.read())
    @self.app.route('/Produtos/<int:id>', methods=['GET'])
    def Search_Produtos(id):
      with Session(Functions.database.engine) as session:
        statement = select(Functions.database.Produtos).where(Functions.database.Produtos.id==id)
        usuario = session.exec(statement).first()
      return jsonify ({
        "id": usuario.id,
        "nome": usuario.nome,
        "preço": usuario.preco,
        "quantidade": usuario.quantidade,
      })

  def run_site(self):
    self.app.run(host='0.0.0.0', port=5000)

bot = Functions.bot.DiscordBot()
site = Site(bot)

bot_thread = Thread(target=bot.start)
bot_thread.daemon = True
bot_thread.start()

site_thread = Thread(target=site.run_site)
site_thread.daemon = True
site_thread.start()

site_thread.join()
bot_thread.join()
