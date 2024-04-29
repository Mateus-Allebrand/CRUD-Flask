from flask import render_template, request, redirect,session,flash,url_for
from jogoteca import app,db
from models import Jogos, Usuarios

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

@app.route("/editar/<int:id>")
def editar(id):
    if "Usuario_logado" not in session or session["Usuario_logado"] == None: 
        return redirect(url_for("login", proxima = url_for("editar"))) #return redirect("/login?proxima=novo") 
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template("editar.html", titulo = "editando Jogo", jogo=jogo)

@app.route("/atualizar", methods = ["POST",])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form["id"]).first()
    jogo.nome = request.form["nome"]
    jogo.categoria = request.form["categoria"]
    jogo.console = request.form["console"]

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/deletar/<int:id>")
def deletar(id):
    if "Usuario_logado" not in session or session["Usuario_logado"] == None: 
        return redirect(url_for("login"))
    
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Jogo deletado com sucesso!")

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
