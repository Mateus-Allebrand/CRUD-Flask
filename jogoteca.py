from flask import Flask,render_template, request, redirect,session,flash


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



#crio uma variavel que vai armazenar a minha aplicação \\\ o __name__ faz referencia a esse proprio arquivo (garante que vai rodar a aplicaçao)
app = Flask(__name__)
app.secret_key = "alumais"

#aqui estou criando uma rota, tenho que criar uma função para dizer o que vai ter nessa rota
@app.route("/")
def index():
    
    return render_template("lista.html",titulo="Jogos", jogos = lista_jogos)  # como não estou lidando apenas com um terminal, preciso colocar aas tags, pois na web lingaugem como "hello World" sem tag, não seria intendido



@app.route("/novo")
def novo():
    return render_template("novo.html", titulo = "Novo Jogo")

@app.route("/criar", methods = ["POST",])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome,categoria,console)
    lista_jogos.append(jogo)

    # return render_template("lista.html", titulo = "Jogos", jogos = lista_jogos) #ao invés desse codigo vou usar redirect
    return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/autenticar", methods=["POST",])
def autenticar():
    if "1234" == request.form["senha"]:
        session["Usuario_logado"] = request.form["usuario"]
        flash(session["Usuario_logado"] + "Logado com sucesso!")
        return redirect("/")
    else:
        flash("Usuario não logado! ")
        return redirect("/login")


#para rodar nossa aplicação temos que finalizar com 
app.run(debug=True)








# Para definir a porta como 8080 e o host como 0.0.0.0 devemos chamar o run da seguinte maneira.

# # trecho da app
# app.run(host='0.0.0.0', port=8080)