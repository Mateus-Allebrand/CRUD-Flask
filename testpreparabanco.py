
import mysql.connector
from mysql.connector import errorcode

print("Conectando...")

try:
    conn = mysql.connector.connect(
        host = "localhost",
        user ="root",
        password = "96465840Mt?"
    )
    print("Conexão bem sucedida!")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erro! Há algo errado com o nome do usuário ou senha")

    else:
        print(err)

cursor = conn.cursor()

# Criar o banco de dados 'jogoteca' se ele não existir
cursor.execute("CREATE DATABASE IF NOT EXISTS jogoteca;")
print("Banco de dados 'jogoteca' criado com sucesso!")


cursor.execute("USE jogoteca;")

#criando tabelas
TABLES = {}

TABLES["Jogos"] = ("""
    CREATE TABLE jogos (
        'id' int(11) = NOT NULL AUTO_INCREMENT, 
        'nome' varchar(50) NOT NULL,
        'categoria' varchar(40) NOT NULL,
        'console' varchar(20) NOT NULL,
        PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;""")

TABLES["Usuarios"] =("""
    CREATE TABLE Usuarios(
    'nome' varchar(30) NOT NULL,        
    'nickname' varchar(20) NOT NULL,
    'senha' varchar(100) NOT NULL,
    PRIMARY KEY (nickname)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;""")
 

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f"Criando tabela {tabela_nome}",end=" ")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Tabela já existe! ")
        else:
            print(err.msg)
    else:
        print("OK")

#inserindo usuários
usuario_sql = "INSERT INTO usuarios (nome, nickname, senha) VALUES (%s,%s,%s);"
usuarios = [("Mateus Allebrand", "Mat", "1234"),
("Mariana Alves", "Mari", "4567"),
("Gabrielli Sena", "Gabi", "1236"),
]

#executemany() está sendo chamado em um objeto do tipo cursor para executar uma instrução SQL usuario_sql várias vezes, uma para cada conjunto de parâmetros na lista usuarios
cursor.executemany(usuario_sql,usuarios)

cursor.execute("SELECT * FROM jogoteca.usuarios;")
print("-=-=-=-=- USUARIOS -=-=-=-=-")
for user in cursor.fetchall():
    print(user[1])


#inserindo jogos
jogos_sql = "INSERT INTO jogos (nome, categoria, console) VALUES (%s,%s,%s);"
jogos =[
("Tetris", "puzly", "Atary"),
("God of war", "Rack n slash", "PS2"),
("Mortal kombat", "Luta", "PS2")
]

cursor.executemany(jogos_sql,jogos)

cursor.execute('select * from jogoteca.jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()