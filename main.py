from flask import Flask, jsonify, session, render_template
import Functions.database
from sqlmodel import Session, null, select

app = Flask(__name__)

@app.route('/')
def Home():
  return render_template('index.html')

@app.route('/Nomes')
def Nomes():
  with Session(Functions.database.engine) as session:
    statement = select(Functions.database.Usuario.nome)
    usuarios = session.exec(statement).all()
    with open('Logs/logNomes.txt', 'w', encoding='utf-8') as arquivo:
      for usuario in usuarios:
        arquivo.write(f'{usuario}\n')
    with open('Logs/logNomes.txt', 'r', encoding='utf-8') as arquivo:
      return jsonify(arquivo.read())

@app.route('/Usuarios')
def Usuarios():
  with Session(Functions.database.engine) as session:
    statement = select(Functions.database.Usuario)
    usuarios = session.exec(statement).all()
    with open('Logs/logUsuarios.txt', 'w', encoding='utf-8') as arquivo:
      for usuario in usuarios:
        arquivo.write(f'{usuario.id},{usuario.nome},{usuario.idade},{usuario.gmail}')
    with open('Logs/logUsuarios.txt', 'r', encoding='utf-8') as arquivo:
      return jsonify(arquivo.read())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
