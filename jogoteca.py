from flask import Flask,render_template, request, redirect,session,flash,url_for


class Jogo:
    def __init__(self, nome, categoria, console):

        self.nome = nome
        self.categoria = categoria
        self.console = console

    # def __str__(self):                  #Dessa maneira daria para resolver
    #     return f"Nome: {self.nome}"
    
jogo01 = Jogo("Tetris", "puzly", "Atary")
jogo02 = Jogo("God of war", "Rack n slash", "PS2")
jogo03 = Jogo("Mortal kombat", "Luta", "PS2")


lista_jogos = [jogo01,jogo02,jogo03]


class Usuario:
    def __init__(self, nome, nickname, senha):
        
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

    

usuario01 = Usuario("Mateus Allebrand", "Mat", "1234")
usuario02 = Usuario("Mariana Alves", "Mari", "4567")
usuario03 = Usuario("Gabrielli Sena", "Gabi", "1236")

usuarios ={usuario01.nome:usuario01,
           usuario02.nome:usuario02,
           usuario03.nome:usuario03}  
 





#crio uma variavel que vai armazenar a minha aplicação \\\ o __name__ faz referencia a esse proprio arquivo (garante que vai rodar a aplicaçao)
app = Flask(__name__)
app.secret_key = "alumais"

#aqui estou criando uma rota, tenho que criar uma função para dizer o que vai ter nessa rota
@app.route("/")
def index():
    
    return render_template("lista.html",titulo="Jogos", jogos = lista_jogos)  # como não estou lidando apenas com um terminal, preciso colocar aas tags, pois na web lingaugem como "hello World" sem tag, não seria intendido


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
    jogo = Jogo(nome,categoria,console)
    lista_jogos.append(jogo)

    # return render_template("lista.html", titulo = "Jogos", jogos = lista_jogos) #ao invés desse codigo vou usar redirect
    return redirect(url_for("index"))

@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)


@app.route("/autenticar", methods=["POST",])
def autenticar():
    if request.form["usuario"] in usuarios:
        usuario = usuarios[request.form["usuario"]]
        
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