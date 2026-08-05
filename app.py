# --------------- VALIDAR GMAILS E CRIAR AS CLASSES (POO) ------------------










# Para criar um banco de dados com o python junto do SQL, devemos usar o seguinte codigo:
import random
import sqlite3

# Usar esse sqlite3.connec é para estabelecer uma conexão com o servidor sql
conexao = sqlite3.connect("Dados.db")
# E para criar um novo arquivo - Vou usar o seguinte codigo:
cursor = conexao.cursor()

cursor.execute(    
    '''
    CREATE TABLE IF NOT EXISTS Login ( 
        id INTEGER PRIMARY KEY,
        Gmail VARCHAR (250),
        Senha VARCHAR (250)
        
        )      
''')


def gerar_id_unico():
    while True:
        # Sorteia um número de 1 a 9999999999 e completa com zeros à esquerda até dar 10 caracteres
        novo_id = str(random.randint(10**9, (10**10) - 1)) # Gera um número entre 1.000.000.000 e 9.999.999.999 (10 dígitos)

        cursor.execute("SELECT 1 FROM Login WHERE id = ?", (novo_id,)) # Busca se o ID sorteado já existe na tabela (usando o '?' para evitar ataques e erros)   

        # Se o banco responder 'Não' (None), o ID é inédito e podemos usá-lo!
        if not cursor.fetchone():
            return novo_id
        # Se o ID já existir, o 'while' repete e sorteia outro número!


# Agora, bora criar uma tabela! -- Basicamente igual o SQL, porém, usar um cursor.execute(codigo em SQL) para coda em SQL


# Para adicionar as coisas no banco de dados:

novo_gmail = str(input("Qual o seu melhor Gmail?: "))
nova_senha = input("Qual a sua senha: ")
# Gerar id do usuario
id_usuario = gerar_id_unico()


# ----- ENTRADA DOS DADOS NO BANCO ------               

#Insrindo os dados no banco

cursor.execute(
    "INSERT INTO Login (id, Gmail, Senha) VALUES (?,?,?)",
    (id_usuario, novo_gmail, nova_senha),
)

# ---- OBRIGATORIO ------ Para salvar tudo agora no banco de dados
conexao.commit()
print(f"\n ✅ O usuário foi cadastrado com sucesso! Seu ID é {id_usuario}\n")


# Para mostrar os dados usamos esse codigo

cursor.execute("SELECT * FROM Login")
mostrar_os_dados = cursor.fetchall()

print("--- DADOS REGISTRADOS ---")
for dados in mostrar_os_dados:
    # Os colchetes e os números [0], [1] e [2] servem para acessar as colunas específicas de cada registro retornado pelo banco de dados
    print(f"ID:{dados[0]}, Gmail:{dados[1]}, Senha:{dados[2]}")

#Sempre fechar a conexão depois do script

conexao.close()
