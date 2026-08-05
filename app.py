# Para criar um banco de dados com o python junto do SQL, devemos usar o seguinte codigo:
import random
import sqlite3

class Banco_de_dados:

    #O __init__ Serve para preparar o terreno e inicializar as variaveis 
    #Basicamente serve para conectar toda vez que a gente entra na classe! 
    def __init__(self, nome_banco = "Dados.db"):

        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    # ===========================================================================

    def criar_tabela(self):
    #Cria a tabela Login no SQLite
        self.cursor.execute(    
            """
            CREATE TABLE IF NOT EXISTS Login ( 
                id INTEGER PRIMARY KEY,
                Gmail VARCHAR (250),
                Senha VARCHAR (250)
                )      
        """)   
        self.conexao.commit()

    # ============================================================================
            
    def validar_Gmail(self, Gmail):

        dominios_valido = [
            "@gmail.com",
            "@hotmail.com",
            "@outlook.com",
            "@yahoo.com",
            ]

        # Se pelo menos um item for verdadeiro, o any() avisa que está OK.  
        return any (Gmail.endswith(dominios) for dominios in dominios_valido)

    # ==========================================================================

    def cadastrar_usuario(self, Gmail, Senha):

        while True:
            id_sorteado = f"{random.randint(1,9999999999):010d}"

            self.cursor.execute("SELECT 1 FROM Login WHERE id = ?", (id_sorteado,))

            if not self.cursor.fetchone():
                break

        #Inserir um novo usuario no banco de dados
        self.cursor.execute(
            "INSERT INTO Login (id, Gmail, Senha) VALUES(?,?,?)", (id_sorteado, Gmail, Senha)
        )
        self.conexao.commit()
        print(f"\n ✅ O usuário foi cadastrado com sucesso! ")
        print(f"\n O seu id cadastrado --> {id_sorteado} ")
                


    # ==========================================================================

    def Listar_usuario(self):
        # Essa função serve para listar todos os usuarios do banco de dados
        self.cursor.execute("SELECT * FROM Login")
        usuarios = self.cursor.fetchall()

        print("\n--- REGISTROS NO BANCO DE DADOS ---")            
        if not usuarios:
            print("(Nenhum cadastro encontrado)")
        else:
            for u in usuarios:
                print(f"ID: {u[0]}, | Gmail: {u[1]}")
        print("-----------------------------------\n")

    # ==========================================================================

    def deletar_usuarios(self, id_usuario):
        #Deletando um usuari do banco, filtrando pelo ID
        self.cursor.execute("DELETE FROM Login WHERE id = ?", (id_usuario,))
        self.conexao.commit()

        if self.cursor.rowcount > 0: 
            print(f"🗑️  Usuário com ID {id_usuario} foi excluído com sucesso!")
        else:
            print(f"⚠️  Nenhum usuário encontrado com o ID {id_usuario}.")

    # ==========================================================================

    def fechar_conexao(self):

        # Essa função serve para fechar o codigo!
        self.conexao.close()        
                



# =====================
# EXECUÇÃO DO PROGRAMA
# =====================

banco = Banco_de_dados()

# -- Cadastro --
print("==== CADASTRAR USUÁRIO ====")

while True:
    gmail_input = input("Qual é o seu melhor Gmail? ").lower().strip()  

    if banco.validar_Gmail(gmail_input):
        break
    else: 
        print( "❌ E-mail inválido! Use um domínio aceito (@gmail.com, @hotmail.com, @outlook.com, @yahoo.com).\n")

senha_input =  input("Digite uma senha: ")


#Executa o trabalho
banco.cadastrar_usuario(gmail_input, senha_input)

#Mostrar a lista atual
banco.Listar_usuario()

# Deletar aqui:

print(" === DELETAR USUÁRIOS ===")
id_deletar = input("Digite o id que você quer excluir: ")
banco.deletar_usuarios(id_deletar)

# Aqui vc vai ver como ficou a lsita depois de excluir o usuário
banco.Listar_usuario()

#Aqui para fechar o banco
banco.fechar_conexao()


