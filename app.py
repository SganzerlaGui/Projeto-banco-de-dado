# Para criar um banco de dados com o python junto do SQL, devemos usar o seguinte codigo:

import sqlite3

# Usar esse sqlite3.connec é para estabelecer uma conexão com o servidor sql

conexao = sqlite3.connect("Dados.db")

# E para criar um novo arquivo - Vou usar o seguinte codigo:

cursor = conexao.cursor()

# Agora, bora criar uma tabela! -- Basicamente igual o SQL, porém, usar um cursor.execute(codigo em SQL) para coda em SQL

cursor.execute(    
    '''
    CREATE TABLE IF NOT EXISTS Login ( 
        id INTEGER PRIMARY KEY,
        Gmail VARCHAR (250),
        Senha VARCHAR (250)
        
        )      
''')

# Para mostrar os dados usamos esse codigo

cursor.execute("SELECT * FROM Login")
mostrar_os_dados = cursor.fetchall()

for dados in mostrar_os_dados:
    print(dados)





#Sempre fechar a conexão depois do script

conexao.close()
