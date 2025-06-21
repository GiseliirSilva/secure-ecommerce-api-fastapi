# API de E-commerce Simplificada com FastAPI

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![JWT](https://img.shields.io/badge/JWT-Authentication-purple.svg)
![Bcrypt](https://img.shields.io/badge/Bcrypt-Hashing-orange.svg)

---

## 📄 Descrição do Projeto

Este projeto consiste em uma API RESTful para um sistema de e-commerce simplificado, desenvolvida com FastAPI. A API permite o gerenciamento de usuários e produtos, incluindo funcionalidades de autenticação (JWT) e autorização baseada em papéis (administrador).

O objetivo principal desta API é fornecer um backend robusto e seguro para futuras aplicações frontend (web ou mobile) ou integrações, demonstrando boas práticas de desenvolvimento backend, modelagem de dados e segurança.

## ✨ Funcionalidades Principais

* **Gerenciamento de Usuários:**
    * Criação de novos usuários (registro).
    * Autenticação de usuários e geração de JWT (JSON Web Token) para acesso seguro.
    * Visualização de usuários (protegido).
    * Atualização e exclusão de usuários (protegido, com permissão de administrador ou próprio usuário).
    * Campo `is_admin` para controle de permissões.
* **Gerenciamento de Produtos:**
    * Criação de novos produtos (protegido, apenas para administradores).
    * Visualização de produtos (todos e por ID).
    * Atualização e exclusão de produtos (protegido, apenas para administradores).
* **Segurança:**
    * Hashing de senhas com `bcrypt`.
    * Autenticação baseada em JWT.
    * Proteção de rotas com requisição de token.
    * Verificação de permissão de `is_admin` para operações sensíveis.
* **Banco de Dados:**
    * Persistência de dados com PostgreSQL.
    * Modelagem e ORM com SQLAlchemy 2.0.

## 🚀 Tecnologias Utilizadas

* **Python 3.13.3** (ou superior)
* **FastAPI**: Framework web moderno e rápido para construir APIs com Python.
* **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional.
* **SQLAlchemy**: Toolkit SQL e Object Relational Mapper (ORM) para Python.
* **Pydantic**: Biblioteca para validação de dados usando type hints do Python.
* **python-dotenv**: Para carregar variáveis de ambiente de um arquivo `.env`.
* **Uvicorn**: Servidor ASGI de alta performance.
* **Bcrypt**: Biblioteca para hash de senhas de forma segura.
* **PyJWT**: Para codificar e decodificar tokens JWT.

## 📁 Estrutura do Projeto

ecommerce_api/
├── .env                  # Variáveis de ambiente (ex: DATABASE_URL, SECRET_KEY)
├── main.py               # Ponto de entrada da API, rotas, lógica principal
├── database/
│   ├── init.py
│   ├── database.py       # Configuração da conexão com o banco de dados (engine, session)
│   └── models.py         # Definição dos modelos ORM (tabelas: User, Product)
├── schemas/
│   ├── init.py
│   ├── auth.py           # Schemas Pydantic para autenticação (TokenRequest, TokenResponse)
│   ├── product.py        # Schemas Pydantic para produtos
│   └── user.py           # Schemas Pydantic para usuários
├── utils/
│   ├── init.py
│   ├── jwt.py            # Funções para manipulação de JWT
│   └── security.py       # Funções de segurança (hashing de senha)
├── venv/                 # Ambiente virtual (gerado após setup)
├── .gitignore            # Arquivos e pastas a serem ignorados pelo Git
└── requirements.txt      # Lista de dependências do projeto


## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

### Pré-requisitos

* Python 3.9+ instalado.
* PostgreSQL instalado e rodando.
* PgAdmin 4 (ou outra ferramenta para gerenciar seu DB PostgreSQL).
* `pip` (gerenciador de pacotes do Python).

### 1. Clonar o Repositório

```bash
git clone [https://github.com/SeuUsuario/ecommerce_api.git](https://github.com/SeuUsuario/ecommerce_api.git)
cd ecommerce_api
(Lembre-se de mudar SeuUsuario/ecommerce_api.git para o link do seu repositório quando você o criar no GitHub)

2. Criar e Ativar o Ambiente Virtual
É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

Bash

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
3. Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

Bash

pip install -r requirements.txt
(Se você ainda não tem o requirements.txt, pode gerá-lo após instalar tudo com pip freeze > requirements.txt)

4. Configurar Variáveis de Ambiente (.env)
Crie um arquivo chamado .env na raiz do projeto (ecommerce_api/) e adicione as seguintes variáveis. Certifique-se de que a DATABASE_URL corresponda à sua configuração do PostgreSQL.

Snippet de código

DATABASE_URL="postgresql://postgres:gicas.1984@localhost:5432/ecommerce"
SECRET_KEY="sua_chave_secreta_aqui_para_jwt" # Troque por uma string aleatória longa
DATABASE_URL: URL de conexão com seu banco de dados PostgreSQL. O ecommerce no final deve ser o nome do banco de dados que você vai criar.
SECRET_KEY: Uma chave secreta longa e aleatória para assinar seus tokens JWT. Você pode gerar uma string aleatória para isso.
5. Configurar o Banco de Dados PostgreSQL
Abra o PgAdmin 4.
Conecte-se ao seu servidor PostgreSQL (geralmente localhost:5432).
Clique com o botão direito em "Databases" (Bancos de Dados) e selecione Create > Database....
Dê o nome ecommerce (EXATAMENTE como na sua DATABASE_URL) ao novo banco de dados e clique em "Save".

▶️ Como Rodar a API
Com o ambiente virtual ativado e as variáveis de ambiente configuradas, inicie o servidor Uvicorn:

Bash

uvicorn main:app --reload --port 8000
--reload: Reinicia o servidor automaticamente ao detectar mudanças no código.
--port 8000: Define a porta em que a API será executada.
Você verá algo como:
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

📚 Documentação da API
A FastAPI gera automaticamente uma documentação interativa no padrão OpenAPI (Swagger UI).
Após iniciar o servidor, acesse:

Swagger UI: http://127.0.0.1:8000/docs
Redoc: http://127.0.0.1:8000/redoc
🧪 Como Testar a API (Usando Postman/Insomnia)
Para interagir com a API, você pode usar ferramentas como Postman ou Insomnia.

Fluxo de Teste Sugerido:
Criar um Usuário (Registro):

Método: POST
URL: http://127.0.0.1:8000/users/
Body (raw, JSON):
JSON

{
  "username": "seu_usuario",
  "email": "seu.email@example.com",
  "password": "sua_senha_segura",
  "full_name": "Seu Nome Completo",
  "disabled": false,
  "is_admin": false
}
Obs: A campo is_admin pode ser omitido, pois o valor padrão é false.
Autenticar e Obter Token:

Método: POST
URL: http://127.0.0.1:8000/token
Body (x-www-form-urlencoded):
username: seu_usuario (ou seu.email@example.com)
password: sua_senha_segura
Resultado: Você receberá um access_token e token_type. Copie o access_token!
Tentar Criar um Produto (Sem ser Admin - Deve Falhar):

Método: POST
URL: http://127.0.0.1:8000/products/
Headers:
Authorization: Bearer SEU_TOKEN_AQUI (Cole o token copiado do passo anterior)
Content-Type: application/json
Body (raw, JSON):
JSON

{
  "name": "Smartphone XPTO",
  "description": "Um smartphone de última geração.",
  "price": 1200.50,
  "stock": 50
}
Resultado Esperado: 403 Forbidden (Você não tem permissão).
Tornar o Usuário Administrador:

Via PgAdmin 4 (Recomendado para este teste):
Abra o PgAdmin 4 e navegue até a tabela users do seu banco de dados ecommerce.
Encontre seu usuário e altere a coluna is_admin de false para true.
Salve as alterações na tabela.
Obter um NOVO Token (Com Permissões de Admin):

Método: POST
URL: http://127.0.0.1:8000/token
Body (x-www-form-urlencoded): Use as mesmas credenciais do usuário que agora é admin.
Resultado: Copie o novo access_token.
Criar um Produto (Com Permissões de Admin - Deve Funcionar):

Método: POST
URL: http://127.0.0.1:8000/products/
Headers:
Authorization: Bearer SEU_NOVO_TOKEN_ADMIN_AQUI
Content-Type: application/json
Body (raw, JSON):
JSON

{
  "name": "Smartphone XPTO",
  "description": "Um smartphone de última geração.",
  "price": 1200.50,
  "stock": 50
}
Resultado Esperado: 201 Created e o JSON do produto criado.
🗄️ Esquema do Banco de Dados
A API utiliza as seguintes tabelas no banco de dados PostgreSQL:

users: Armazena informações dos usuários.
id (PK), username (Único), email (Único), hashed_password, full_name, disabled, is_admin.
products: Armazena informações dos produtos.
id (PK), name, description, price, stock.
👩‍💻 Autor
Giseli (Estudante de Análise e Desenvolvimento de Sistemas com foco em Backend e Automação com Python)

