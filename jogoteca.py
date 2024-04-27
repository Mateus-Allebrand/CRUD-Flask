from flask import Flask,render_template, request, redirect,session,flash,url_for
from flask_sqlalchemy import SQLAlchemy


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
app.secret_key = "alumais"


app.config["SQLALCHEMY_DATABASE_URI"] = \
"{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(
SGBD = "mysql+mysqlconnector",
usuario = "root",
senha = "96465840Mt?",
servidor = "localhost",
database = "jogoteca"
)

db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome = db.Column(db.String(50),nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return "<name %r" %self.name


class Usuarios(db.Model):
    nickname = db.Column(db.String(20),primary_key=True)
    nome = db.Column(db.String(50),nullable=False)
    senha = db.Column(db.String(100),nullable=False)
    

    def __repr__(self):
        return "<name %r" %self.name




#aqui estou criando uma rota, tenho que criar uma função para dizer o que vai ter nessa rota
@app.route("/")
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template("lista.html",titulo="Jogos", jogos = lista)  # como não estou lidando apenas com um terminal, preciso colocar aas tags, pois na web lingaugem como "hello World" sem tag, não seria intendido


@app.route("/novo")
def novo():
    if "Usuario_logado" not in session or session["Usuario_logado"] == None: 
        return redirect(url_for("login", proxima = url_for("novo"))) #return redirect("/login?proxima=novo") 
    return render_template("novo.html", titulo = "Novo Jogo")

@app.route("/criar", methods = ["POST",])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
     
    #verificando se o jogo que vou incluir já existe em meu banco de dados    #cod antes era assim =>  jogo = Jogo(nome,categoria,console)
    jogo = Jogos.query.filter_by(nome=nome).first()                           #cod antes era assim =>  lista_jogos.append(jogo)

    if jogo:
        flash("O jogo já existe na lista")
        return redirect(url_for("index"))                                                          
                                                                            # return render_template("lista.html", titulo = "Jogos", jogos = lista_jogos) #ao invés desse codigo vou usar redirect
    novo_jogo = Jogos(nome=nome, categoria=categoria,console=console)
    db.session.add(novo_jogo)
    db.session.commit()
    return redirect(url_for("index")) 

@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)


@app.route("/autenticar", methods=["POST",])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form["usuario"]).first()

    if usuario:                          #nessa linha eras assim => request.form["usuario"] in usuarios: antes do db
                                         #nessa linha eras assim => usuario = usuarios[request.form["usuario"]] antes do db
        if request.form["senha"] == usuario.senha:
            session["Usuario_logado"] = usuario.nickname 
            flash(usuario.nickname + "Logado com sucesso!")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina) #"/{}".format(proxima_pagina)
        
    else:
        flash("Usuario não logado! ")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session["Usuario_logado"] = None
    flash("Logout efefuado com sucesso! ")
    return redirect(url_for("index"))


#para rodar nossa aplicação temos que finalizar com 
app.run(debug=True)








# Para definir a porta como 8080 e o host como 0.0.0.0 devemos chamar o run da seguinte maneira.

# # trecho da app
# app.run(host='0.0.0.0', port=8080)