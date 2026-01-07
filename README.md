

# Gestor de Lacres 🔐

Projeto para gerenciamento, rastreamento e conciliação de lacres operacionais.

## 🎯 Objetivo
Criar uma base centralizada de lacres, permitindo:
- Geração de lacres sequenciais
- Cadastro de lacres novos
- Importação de base bruta de lacres utilizados
- Conciliação automática entre lacres gerados e utilizados

## 🧩 Módulos do Projeto

### 1. Coleta de Base Bruta
Robô responsável por acessar uma página web e coletar dados de lacres utilizados.

### 2. Gerador de Lacres
Script que gera sequências de lacres (alfanuméricos) a partir de um número inicial e final.

### 3. Banco de Dados
Banco central para controle de status dos lacres:
- NOVO
- UTILIZADO
- INVALIDADO

### 4. Conciliação
Cruzamento entre a base bruta e os lacres cadastrados, atualizando o status automaticamente.

## 🗂 Estrutura do Projeto


## 🚀 Tecnologias
- Python
- Pandas
- Selenium
- PostgreSQL / SQLite (fase inicial)

## 📌 Status
🚧 Em desenvolvimento
