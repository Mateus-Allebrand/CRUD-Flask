from flask import render_template, request, redirect,session,flash,url_for, send_from_directory
from jogoteca import app,db
from models import Jogos
from helpers import recupera_imagem,deleta_arquivo, FormularioJogo
import time


#aqui estou criando uma rota, tenho que criar uma função para dizer o que vai ter nessa rota
@app.route("/")
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template("lista.html",titulo="Jogos", jogos = lista)  # como não estou lidando apenas com um terminal, preciso colocar aas tags, pois na web lingaugem como "hello World" sem tag, não seria intendido

#
@app.route("/novo")
def novo():
    if "Usuario_logado" not in session or session["Usuario_logado"] == None: 
        return redirect(url_for("login", proxima = url_for("novo"))) #return redirect("/login?proxima=novo") 
    
    form = FormularioJogo()

    return render_template("novo.html", titulo = "Novo Jogo", form=form)



@app.route("/criar", methods = ["POST",])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for("novo"))


    nome = form.nome.data                             #nome = request.form["nome"]
    categoria = form.categoria.data                   # categoria = request.form["categoria"]
    console = form.console.data                       # console = request.form["console"]
     
    #verificando se o jogo que vou incluir já existe em meu banco de dados    #cod antes era assim =>  jogo = Jogo(nome,categoria,console)
    jogo = Jogos.query.filter_by(nome=nome).first()                           #cod antes era assim =>  lista_jogos.append(jogo)

    if jogo:
        flash("O jogo já existe na lista")
        return redirect(url_for("index"))                                                          
                                                                            # return render_template("lista.html", titulo = "Jogos", jogos = lista_jogos) #ao invés desse codigo vou usar redirect
    novo_jogo = Jogos(nome=nome, categoria=categoria,console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files["arquivo"]
    #arquivo.save(f"uploads/{arquivo.filename}") vou melhorar isso para não dar conflito
    upload_path = app.config["UPLOAD_PATH"]
    timestemp = time.time()
    arquivo.save(f"{upload_path}/capa{novo_jogo.id}-{timestemp}.jpg")

    return redirect(url_for("index")) 

@app.route("/editar/<int:id>")
def editar(id):
    if "Usuario_logado" not in session or session["Usuario_logado"] == None: 
        return redirect(url_for("login", proxima = url_for("editar"))) #return redirect("/login?proxima=novo") 
    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)

    return render_template("editar.html", titulo = "editando Jogo", id=id, capa_jogo=capa_jogo, form=form)

# @app.route('/editar/<int:id>')
# def editar(id):
#     if 'usuario_logado' not in session or session['usuario_logado'] == None:
#         return redirect(url_for('login', proxima=url_for('editar', id=id)))
#     jogo = Jogos.query.filter_by(id=id).first()
#     capa_jogo = recupera_imagem(id)
#     return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route("/atualizar", methods = ["POST",])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form["id"]).first()
        jogo.nome = form.nome.data                  #request.form["nome"]
        jogo.categoria = form.categoria.data             #request.form["categoria"]
        jogo.console = form.console.data               #request.form["console"]

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files["arquivo"]
        upload_path = app.config["UPLOAD_PATH"]
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f"{upload_path}/capa{jogo.id}-{timestamp}.jpg")

    return redirect(url_for("index"))

@app.route("/deletar/<int:id>")
def deletar(id):
    if "Usuario_logado" not in session or session["Usuario_logado"] == None: 
        return redirect(url_for("login"))
    
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Jogo deletado com sucesso!")

    return redirect(url_for("index"))




@app.route("/uploads/<nome_arquivo>")
def imagem(nome_arquivo):
    return send_from_directory("uploads", nome_arquivo)
