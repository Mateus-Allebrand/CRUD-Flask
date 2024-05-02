from flask import render_template, request, redirect,session,flash,url_for
from jogoteca import app
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash



@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    form = FormularioUsuario()
    return render_template("login.html", proxima=proxima, form=form)



@app.route("/autenticar", methods=["POST",])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()  #request.form["usuario"] foi substituido por form.nickname.data
    senha = check_password_hash(usuario.senha, form.senha.data)

    if usuario and senha:                           #nessa linha eras assim => request.form["usuario"] in usuarios: antes do db
                                                    #nessa linha eras assim => usuario = usuarios[request.form["usuario"]] antes do db
                                                       #  request.form["senha"] foi subs por form.senha.data
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