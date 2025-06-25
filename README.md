# Sistema de Gestão de Vendas e Estoque

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-concluído-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> 🏆 **Projeto Concluído** 🏆

## 📝 Descrição

Este projeto é um sistema de Ponto de Venda (PDV) e gestão de estoque desenvolvido em Python, com uma interface gráfica moderna construída com a biblioteca **CustomTkinter**. O objetivo inicial era simular as operações de uma loja via console, aplicando conceitos de raciocínio algorítmico, mas o projeto evoluiu para uma aplicação de desktop completa e funcional.

A arquitetura do sistema foi projetada para uma clara **separação de camadas**:
* **Backend (`modules/`):** Uma lógica de negócio "headless" (sem interface) que gerencia usuários, produtos, vendas e relatórios.
* **Frontend (`interface/`):** Uma interface gráfica orientada a objetos que consome os serviços do backend para proporcionar uma experiência de usuário intuitiva.
* **Dados (`data/`):** Persistência de dados através de arquivos CSV e JSON.

Este trabalho foi desenvolvido para a disciplina de Raciocínio Algorítmico.

## ✨ Funcionalidades Implementadas

#### 🧑‍💼 Módulo 1: Gestão de Usuários e Acesso
- [x] Cadastro e Login de usuários.
- [x] Diferenciação de níveis de acesso (Admin vs. Vendedor).
- [x] CRUD completo de usuários (Cadastrar, Listar, Excluir) via interface de admin.
- [x] Setup gráfico para criação do primeiro usuário administrador.

#### 📦 Módulo 2: Gestão de Produtos
- [x] CRUD completo de produtos (Cadastrar, Listar, Editar, Excluir).
- [x] Gerenciamento de informações como preço de custo, preço de venda e quantidade.
- [x] Função de reposição de estoque para o administrador.

#### 🛒 Módulo 3: Operações de Venda
- [x] Interface de venda com carrinho de compras interativo (adicionar/remover itens).
- [x] Atualização automática de estoque após cada venda.
- [x] Validação de estoque em tempo real para prevenir vendas indevidas.

#### 📈 Módulo 4: Financeiro e Relatórios
- [x] Cálculo e registro de lucro em cada venda.
- [x] Registro de todas as transações (vendas e compras/reposição).
- [x] Geração de relatório de vendas diárias com faturamento e lucro.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Interface Gráfica:** CustomTkinter, Tkinter (`messagebox`, `simpledialog`)
* **Persistência de Dados:** Módulos `json` e `csv` da biblioteca padrão.

## 🚀 Como Executar o Projeto

Para executar este projeto localmente, siga os passos abaixo.

**1. Pré-requisitos:**
* Ter o [Python 3](https://www.python.org/downloads/) e o `pip` instalados.
* Ter o `git` instalado para clonar o repositório.

**2. Instalação:**

```bash
# Clone o repositório para sua máquina local
git clone [https://github.com/R3I5/ProjetoFinalRacAlgoritmico.git](https://github.com/R3I5/ProjetoFinalRacAlgoritmico.git)

# Navegue até a pasta do projeto
cd ProjetoFinalRacAlgoritmico

# Crie um ambiente virtual (altamente recomendado)
python3 -m venv venv

# Ative o ambiente virtual
# No Windows: venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instale todas as dependências necessárias
pip install -r requirements.txt
```

**3. Execução:**

Com o ambiente virtual ativado, execute o seguinte comando para iniciar a aplicação gráfica:
```bash
python run_gui.py
```
*Se for a primeira execução, uma série de diálogos aparecerá para configurar a conta do administrador.*

## 📂 Estrutura do Projeto

```
/ProjetoFinalRacAlgoritmico
├── data/
│   ├── produtos.csv
│   ├── transacoes.json
│   └── usuarios.json
├── interface/
│   ├── __init__.py
│   ├── app.py
│   ├── tela_login.py
│   ├── tela_principal.py
│   └── ... (outras telas .py)
├── modules/
│   ├── usuarios.py
│   ├── produtos.py
│   └── ... (outros módulos .py)
├── run_gui.py            # <-- Ponto de entrada da aplicação
├── README.md
└── requirements.txt
```

## 👨‍💻 Autor

Feito por **João Victor dos Reis**.
