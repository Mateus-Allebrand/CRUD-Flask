from flask import Flask,render_template



#crio uma variavel que vai armazenar a minha aplicação \\\ o __name__ faz referencia a esse proprio arquivo (garante que vai rodar a aplicaçao)
app = Flask(__name__)

#aqui estou criando uma rota, tenho que criar uma função para dizer o que vai ter nessa rota
@app.route("/inicio")
def ola():
    lista_jogos = ["God of War", "Mario World", "Crash"]

    return render_template("lista.html",titulo="Jogos", jogos = lista_jogos)  # como não estou lidando apenas com um terminal, preciso colocar aas tags, pois na web lingaugem como "hello World" sem tag, não seria intendido






#para rodar nossa aplicação temos que finalizar com 
app.run()








# Para definir a porta como 8080 e o host como 0.0.0.0 devemos chamar o run da seguinte maneira.

# # trecho da app
# app.run(host='0.0.0.0', port=8080)