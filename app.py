# Para criar um banco de dados com o python junto do SQL, devemos usar o seguinte codigo:
import random
import sqlite3
from fastapi import FastAPI
from google import genai
from pydantic import BaseModel

ia = FastAPI()

# Configuração do Cliente Gemini
# RECOMENDAÇÃO: Lembre-se de usar a sua chave atualizada do Google AI Studio aqui
cliente = genai.Client(api_key="Sua chave do gimini aqui")

class Perguntas(BaseModel):
    texto: str

@ia.post("/perguntar")
def resposta_do_gemini(pergunta: Perguntas):
    resposta_ia = cliente.models.generate_content(
        model='gemini-3.6-flash',
        contents=pergunta.texto
    )

    texto_resposta = resposta_ia.text

    return {
        "status": "sucesso",
        "provedor": "Google Gemini",
        "resposta": texto_resposta
    }

class Banco_de_dados:

    #O __init__ Serve para preparar o codigo e inicializar as variaveis 
    #Basicamente serve para conectar toda vez que a gente entra na classe/ ele sempre vai criar 3 coisas quando entramos na classe, abre o banco, escreve no sql e já chama a função para criar a tabela no sql
    def __init__(self, nome_banco = "Dados.db"):
        self.conexao = sqlite3.connect(nome_banco) # ---> self.conexao: Abre o arquivo do banco.
        self.cursor = self.conexao.cursor()         # --->  self.cursor: Cria o "ponteiro/caneta" que vai escrever os comandos SQL
        self.criar_tabela()                         # ---> self.criar_tabela(): Ele já chama a função de criar a tabela logo em seguida, para garantir que o banco não comece vazio.

    # ===========================================================================

    def criar_tabela(self):
    #Cria a tabela Login no SQLite com a nova coluna Nome
        self.cursor.execute(    
            """
            CREATE TABLE IF NOT EXISTS Login ( 
                id INTEGER PRIMARY KEY,
                Gmail VARCHAR (250),
                Senha VARCHAR (250),
                Nome VARCHAR (500)
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

    def cadastrar_usuario(self, Gmail, Senha, nome):
        self.cursor.execute("SELECT 1 FROM Login WHERE Gmail = ?", (Gmail,))
        usuario_existente = self.cursor.fetchone()  # O fetchone() serve para resgatar o primeiro resultado que o banco de dados encontrou! Se ele voltar preenchido, a informação já existe. Se voltar vazio (None), ela não existe!

        if usuario_existente:
            print(f"\n❌ Erro: O gmail {Gmail}, já foi cadastrado no sistema!")
            return False       # <--- Retorna False avisando que o cadastro FALHOU

        # Sorteia um ID livre no sistema
        while True:
            id_sorteado = f"{random.randint(1,9999999999):010d}"
            self.cursor.execute("SELECT 1 FROM Login WHERE id = ?", (id_sorteado,))
            if not self.cursor.fetchone():
                break

        # CORREÇÃO DE IDENTAÇÃO: Essas linhas agora estão FORA do while True acima!
        # O python tenta inserir os dados no banco -- O id que foi sorteado, o gmail, a senha e o nome
        self.cursor.execute(
            "INSERT INTO Login (id, Gmail, Senha, Nome) VALUES(?,?,?,?)", (id_sorteado, Gmail, Senha, nome)
        )
        self.conexao.commit()
        print(f"\n ✅ O usuário foi cadastrado com sucesso! ")
        return True    # return True: Quando o código passa por todas as checagens e consegue salvar no banco!

    # ==========================================================================
    # Nova função que coleta os dados locais e faz o meio-campo com o Gemini
    def assistente_ia(self, pergunta_dono):
         # Busca apenas a coluna Gmail de todo mundo no banco
        self.cursor.execute("SELECT Gmail FROM Login")
        linhas = self.cursor.fetchall()
        
        # Converte os dados do SQLite em uma string que a IA consegue ler
        if not linhas:
            Listar_usuario = "Nenhum usuário cadastrado no momento."
        else:
            # CORREÇÃO: Espaço adicionado antes do 'for' para evitar erro de sintaxe
            Listar_usuario = "\n".join([u[0] for u in linhas])

        contexto_sistema = f"""
        Você é o assistente virtual de TI e RH de uma empresa.
        Abaixo está a lista completa e updated de TODOS os e-mails cadastrados no banco de dados local:

        {Listar_usuario}
            
        O dono da empresa vai te fazer uma pergunta. Analise a lista e responda de forma direta e natural.
        """

        # Envia o pacote completo para o modelo do Gemini processar
        try:
            resposta_ia = cliente.models.generate_content(
                model='gemini-3.6-flash',
                contents=f"{contexto_sistema}\n\nPergunta do Dono: {pergunta_dono}"
            )
            return resposta_ia.text  # Retorna apenas o texto limpo gerado pela IA
        except Exception as e:
            return f"❌ Erro ao conectar com o Gemini: {e}" 

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
                print(f"ID: {u[0]}, | Gmail: {u[1]} | Nome: {u[3]}")
        print("-----------------------------------\n")

    # ==========================================================================

    def deletar_usuarios(self, id_usuario):
        #Deletando um usuário do banco, filtrando pelo ID
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
    print("\n=== MENU DE OPÇÕES ===")
    print("1 - Cadastra novo usuário")
    print("2 - Excluir conta")
    print("3 - Listar contas")
    print("4 - Assistente IA (Perguntar ao Gemini) 🤖")
    print("5 - Sair")

banco = Banco_de_dados()

# Menu interativo
while True:
    Menu()
    escolha = input("\nEscolha uma opção: ").strip() #---> Serve para tirar as linhas que foram dado espaço

    # CORREÇÃO: Números do menu comparados como String ("1", "2", etc.)
    if escolha == "1":
        print("\n==== CADASTRAR USUÁRIO ====")

        while True:
            nome_input = input("Qual o seu nome? ").strip()
            gmail_input = input("Qual é o seu Gmail? ").lower().strip()  
            senha_input = input("Digite uma senha: ")

            # Primeiro ele vê SE NÃO for válido
            if not banco.validar_Gmail(gmail_input):
                print(f"❌ O gmail: {gmail_input} que o Sr(a) colocou não é válido! Use um domínio aceito (@gmail.com, etc).\n")
                continue
            
            # Se o e-mail for válido no formato, sai do loop de perguntas
            break
        
        # CORREÇÃO DO FLUXO: Executa o cadastro real uma única vez fora do loop de inputs!
        banco.cadastrar_usuario(gmail_input, senha_input, nome_input)

    elif escolha == "2":
        print("\n=== DELETAR USUÁRIO ===")
        id_deletar = input("Digite o ID que você quer excluir: ")
        banco.deletar_usuarios(id_deletar)

    elif escolha == "3":
        banco.Listar_usuario()

    elif escolha == "4":
        print("\n🤖 [Assistente IA] Olá, Diretor! O que deseja saber sobre a nossa base de dados?")
        pergunta = input("Sua pergunta: ")
        
        print("\n⏳ Consultando o banco de dados")
        resposta_final = banco.assistente_ia(pergunta)
        
        print("\n--- RESPOSTA DO ASSISTENTE ---")
        print(resposta_final)
        print("------------------------------")

    elif escolha == "5":
        print("\n👋 Encerrando o sistema... Até logo!")
        banco.fechar_conexao()
        break
        
    else:
        print("❌ Opção inválida! Escolha um número de 1 a 5.")
