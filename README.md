# Sistema de Gestão de Vendas e Estoque (PDV em Console)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Status](https://img.shields.io/badge/status-em_desenvolvimento-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> 🚧 **Projeto em Desenvolvimento** 🚧

## 📝 Descrição

Este projeto é um sistema de Ponto de Venda (PDV) e gestão de estoque desenvolvido em Python, executado inteiramente no console (terminal). O objetivo é simular as operações de uma loja, aplicando conceitos fundamentais de lógica de programação, estrutura de dados e manipulação de arquivos.

Este trabalho está sendo desenvolvido para a disciplina de Raciocínio Algorítmico.

## ✨ Funcionalidades

O sistema foi projetado com os seguintes módulos e funcionalidades:

#### 🧑‍💼 **Módulo 1: Gestão de Usuários e Acesso**
- [x] Cadastro e Login de usuários.
- [ ] Diferenciação de níveis de acesso (Admin vs. Vendedor).

#### 📦 **Módulo 2: Gestão de Produtos (CRUD)**
- [x] Cadastro de novos produtos (Nome, Categoria, Preço, Estoque).
- [x] Consulta de produtos.
- [ ] Edição de informações de produtos existentes.
- [ ] Exclusão de produtos.

#### 🛒 **Módulo 3: Operações de Venda e Estoque**
- [x] Registro de vendas com atualização automática de estoque.
- [x] Verificação de disponibilidade de estoque antes da venda.
- [ ] Reposição de estoque (entrada de mercadorias).

#### 📈 **Módulo 4: Financeiro e Relatórios**
- [ ] Consulta de Caixa (saldo total das vendas).
- [ ] Cálculo de lucro por venda.
- [ ] Geração de relatório de produtos com estoque baixo.
- [ ] Geração de extratos de transações com filtros (diário, mensal, etc.).


## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Persistência de Dados:** Arquivos de texto em formato CSV ou JSON (a ser definido).

## 🚀 Como Executar o Projeto

Para executar este projeto localmente, siga os passos abaixo:

**1. Pré-requisitos:**
* Certifique-se de ter o [Python 3](https://www.python.org/downloads/) instalado.
* É recomendado o uso de um ambiente virtual (`venv`).

**2. Clone o repositório:**
```bash
git clone https://github.com/R3I5/ProjetoFinalRacAlgoritmico.git
cd ProjetoFinalRacAlgoritmico
