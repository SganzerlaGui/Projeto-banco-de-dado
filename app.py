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
        novo_id = str(random.randint(1,9999999999)).zfill(10) # O .zfill(numero) --- serve para que complete com 0... até completar 10 digitos

        cursor.execute("SELECT 1 FROM Login WHERE id = ?", (novo_id,)) # Busca se o ID sorteado já existe na tabela (usando o '?' para evitar ataques e erros)   

        # Se o banco responder 'Não' (None), o ID é inédito e podemos usá-lo!
        if not cursor.fetchone():
            return novo_id
        # Se o ID já existir, o 'while' repete e sorteia outro número!


# Agora, bora criar uma tabela! -- Basicamente igual o SQL, porém, usar um cursor.execute(codigo em SQL) para coda em SQL


# Para adicionar as coisas no banco de dados:

novo_gmail = str(input("Qual o seu melhor Gmail?: "))
nova_senha = input("Qual a sua senha: ")





# Para mostrar os dados usamos esse codigo

cursor.execute("SELECT * FROM Login")
mostrar_os_dados = cursor.fetchall()

for dados in mostrar_os_dados:
    print(dados)

#Sempre fechar a conexão depois do script

conexao.close()
