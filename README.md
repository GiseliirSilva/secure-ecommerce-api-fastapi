# 🛒 API de E-commerce com FastAPI

## 📌 Sobre o projeto

Desenvolvimento de uma API RESTful para gerenciamento de usuários e produtos, com foco em segurança, organização de dados e aplicação de regras de negócio.

A API simula o funcionamento de um sistema de e-commerce, permitindo controle de acesso, autenticação de usuários e operações protegidas.

---

## 🎯 Objetivo

* Desenvolver uma API com boas práticas de backend
* Implementar autenticação e controle de acesso
* Aplicar regras de negócio em operações sensíveis
* Estruturar dados para persistência e integração

---

## 🛠️ Tecnologias utilizadas

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT (autenticação)
* Bcrypt (segurança de senhas)

---

## 🔐 Principais funcionalidades

### 👤 Usuários

* Cadastro de usuários
* Autenticação com geração de token JWT
* Atualização e exclusão com controle de acesso

### 🛍️ Produtos

* Cadastro de produtos (restrito a administrador)
* Listagem e consulta por ID
* Atualização e exclusão com validação de permissão

### 🔒 Segurança

* Hash de senhas com Bcrypt
* Autenticação via JWT
* Proteção de rotas
* Controle de permissões (admin)

---

## 📊 Resultados e aprendizados

* Aplicação prática de autenticação e autorização
* Estruturação de API com separação de camadas
* Modelagem de dados com ORM
* Desenvolvimento de sistema com foco em segurança

---

## 📌 Diferencial do projeto

A API implementa controle de acesso baseado em perfil de usuário, simulando cenários reais de aplicações corporativas com autenticação segura e validação de permissões.

---

## ⚙️ Estrutura do projeto

* `main.py` → rotas e inicialização
* `database/` → conexão e modelos
* `schemas/` → validação de dados
* `utils/` → autenticação e segurança

---

## 🚀 Como executar

```bash
uvicorn main:app --reload
```

Acesse:

* http://127.0.0.1:8000/docs

---

## 📌 Observação

Projeto com finalidade prática, aplicando conceitos de desenvolvimento backend, segurança e organização de sistemas.

---

## 👩‍💻 Autora

**Giseli Silva**
Área Administrativa | Dados | Python




