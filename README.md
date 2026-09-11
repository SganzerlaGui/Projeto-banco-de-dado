# 🗄️ Sistema de Gestão de Usuários & Assistente IA com FastAPI, SQLite e Gemini

> Aplicação em Python que combina um sistema completo de gerenciamento de banco de dados SQLite (CRUD com validações) e uma API FastAPI integrada ao Google Gemini SDK para análise interativa de dados em tempo real.

---

## 📌 Sobre o Projeto

O projeto foi desenvolvido com foco em arquitetura de software, orientação a objetos (POO) e integração com inteligência artificial generativa. 

A aplicação gerencia cadastros de usuários locais em um banco de dados **SQLite** e fornece uma interface de terminal alimentada pela API do **Google Gemini**, que atua como assistente virtual consultando os registros do banco em tempo real para responder a dúvidas de gestão e RH.

### 🛠️ Funcionalidades Principais:
- [x] **API com FastAPI:** Endpoint HTTP `/perguntar` construído para processar requisições para a IA via Pydantic.
- [x] **CRUD no SQLite:** Métodos estruturados em POO para criação de tabelas, inserção, listagem e remoção por ID.
- [x] **Validação e Regras de Negócio:** Algoritmo de validação de domínios de e-mail e checagem de duplicidade no banco.
- [x] **Geração de IDs Únicos:** Sorteio e verificação dinâmica de IDs de 10 dígitos.
- [x] **Assistente IA Integrado:** Integração com `google-genai` que constrói um contexto dinâmico dos dados cadastrados e responde a perguntas analíticas do gestor.

---

## 💻 Tecnologias e Ferramentas

- **Linguagem:** Python 3.x
- **Framework Web / API:** FastAPI, Pydantic
- **Banco de Dados:** SQLite (`sqlite3`)
- **Inteligência Artificial:** Google GenAI SDK (`google-genai` / Modelo `gemini-2.5-flash`)
- **Versionamento:** Git / GitHub

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python instalado na sua máquina (versão 3.10+ recomendada).
- Uma chave de API do **Google AI Studio** (API Key).

### Passo a Passo

1. **Clonar o repositório:**
```bash
git clone [https://github.com/SganzerlaGui/Projeto-banco-de-dado.git](https://github.com/SganzerlaGui/Projeto-banco-de-dado.git)
cd Projeto-banco-de-dado
