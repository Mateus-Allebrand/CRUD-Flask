from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

#no inicio usei esse codigo para criar as classes, agora foi substituido por classe jogos e usuarios com db
# class Jogo:
#     def __init__(self, nome, categoria, console):

#         self.nome = nome
#         self.categoria = categoria
#         self.console = console

#     # def __str__(self):                  #Dessa maneira daria para resolver
#     #     return f"Nome: {self.nome}"
    
# jogo01 = Jogo("Tetris", "puzly", "Atary")
# jogo02 = Jogo("God of war", "Rack n slash", "PS2")
# jogo03 = Jogo("Mortal kombat", "Luta", "PS2")


# lista_jogos = [jogo01,jogo02,jogo03]


# class Usuario:
#     def __init__(self, nome, nickname, senha):
        
#         self.nome = nome
#         self.nickname = nickname
#         self.senha = senha

    

# usuario01 = Usuario("Mateus Allebrand", "Mat", "1234")
# usuario02 = Usuario("Mariana Alves", "Mari", "4567")
# usuario03 = Usuario("Gabrielli Sena", "Gabi", "1236")

# usuarios ={usuario01.nome:usuario01,
#            usuario02.nome:usuario02,
#            usuario03.nome:usuario03}  
 

#crio uma variavel que vai armazenar a minha aplicação \\\ o __name__ faz referencia a esse proprio arquivo (garante que vai rodar a aplicaçao)
app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from views_game import *
from views_user import *

if __name__ == "__main__":
    #para rodar nossa aplicação temos que finalizar com 
    app.run(debug=True)

# Para definir a porta como 8080 e o host como 0.0.0.0 devemos chamar o run da seguinte maneira.

# # trecho da app
# app.run(host='0.0.0.0', port=8080)