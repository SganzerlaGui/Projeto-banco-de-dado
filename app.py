# Para criar um banco de dados com o python junto do SQL, devemos usar o seguinte codigo:
import random
import sqlite3

class Banco_de_dados:

    #O __init__ Serve para preparar o codigo e inicializar as variaveis 
    #Basicamente serve para conectar toda vez que a gente entra na classe/ ele sempre vai criar 3 coisas quando entramos na classe, abre o banco, escreve no sql e já chama a função para criar a tabela no sql
    def __init__(self, nome_banco = "Dados.db"):

        self.conexao = sqlite3.connect(nome_banco) # ---> self.conexao: Abre o arquivo do banco.
        self.cursor = self.conexao.cursor()         # --->  self.cursor: Cria o "ponteiro/caneta" que vai escrever os comandos SQL
        self.criar_tabela()                         # ---> self.criar_tabela(): Ele já chama a função de criar a tabela logo em seguida, para garantir que o banco não comece vazio.

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
        self.cursor.execute("SELECT 1 FROM login where Gmail = ?", (Gmail,))
        usuario_existente = self.cursor.fetchone()  # O fetchone() serve para resgatar o primeiro resultado que o banco de dados encontrou! Se ele voltar preenchido, a informação já existe. Se voltar vazio (None), ela não existe!

        if usuario_existente:
            print(f"Erro: O gmail {Gmail}, já foi cadastrado no sistema!")
            return False       # <--- Retorna False avisando que o cadastro FALHOU ----- return False: Quando o código descobre que o e-mail já existe, ele grita: "Opa, deu erro!" e para tudo.


        while True:
            id_sorteado = f"{random.randint(1,9999999999):010d}"

            self.cursor.execute("SELECT 1 FROM Login WHERE id = ?", (id_sorteado,))

            if not self.cursor.fetchone():
                break

            #O python tenta inserir os dados no banco -- O id que foi sorteado, o gmail e a senha
            self.cursor.execute(
                "INSERT INTO Login (id, Gmail, Senha) VALUES(?,?,?)", (id_sorteado, Gmail, Senha)
            )
            self.conexao.commit()
            print(f"\n ✅ O usuário foi cadastrado com sucesso! ")
            print(f"\n O seu id cadastrado --> {id_sorteado} ")
            return True    # return True: Quando o código passa por todas as checagens e consegue salvar no banco, ele grita: "Sucesso, deu tudo certo!".


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

def Menu():
   
        print("\n=== CADASTROS DEPARTAMENTOS ===\n")

        print("\nEscolha a opção desejada\n")

        print("\n1 - Cadastra novo usuário")

        print("\n2 - Excluir conta")

        print("\n3 - Listar contas")

        print("\n4 - Modificar senha")

        print("\n5 - Sair")


banco = Banco_de_dados()

#Menu interativo
while True:
    Menu()
    escolha = input("Esscolha uma opção: ").strip()

    if escolha == 1:
            # -- Cadastro --
        print("==== CADASTRAR USUÁRIO ====")

        while True:
        
            gmail_input = input("Qual é o seu Gmail? ").lower().strip()  

            senha_input =  input("Digite uma senha: ")


            # Primeiro ele vê SE NÃO 
            if not banco.validar_Gmail(gmail_input):
                print(f"O gmail: {gmail_input} que o Sr(a) colocou não é valido! Use um domínio aceito")
                continue
            
            if banco.cadastrar_usuario(gmail_input, senha_input):
                print(f"O gmail: {gmail_input}, já está cadastrado em nosso sistema. ")
                continue
            
            break
        
        
        
        #Executa o trabalho
        banco.cadastrar_usuario(gmail_input, senha_input)

        #Mostrar a lista atual
        banco.Listar_usuario()

    elif escolha == 2:
                # Deletar aqui:
        print(" === DELETAR USUÁRIOS ===")
        id_deletar = input("Digite o id que você quer excluir: ")
        banco.deletar_usuarios(id_deletar)

        # Aqui vc vai ver como ficou a lsita depois de excluir o usuário
        banco.Listar_usuario()

        #Aqui para fechar o banco
        banco.fechar_conexao()



    elif escolha == 3:
        continue

