# modules/produtos.py

import csv
import os
from datetime import datetime
from modules.utils import obter_input_texto, obter_input_numerico, obter_input_numerico_opcional # Importando as validações
from modules import transacoes # Import para registrar a transação de compra

CAMINHO_ARQUIVO_PRODUTOS = os.path.join('data', 'produtos.csv')
CABECALHO = ['id', 'nome', 'preco_custo', 'preco_venda', 'estoque']

def load_products():
    if not os.path.exists(CAMINHO_ARQUIVO_PRODUTOS): return []
    produtos = []
    try:
        with open(CAMINHO_ARQUIVO_PRODUTOS, 'r', encoding='utf-8', newline='') as f:
            leitor_csv = csv.DictReader(f)
            for linha in leitor_csv:
                linha['id'] = int(linha['id'])
                linha['preco_custo'] = float(linha['preco_custo'])
                linha['preco_venda'] = float(linha['preco_venda'])
                linha['estoque'] = int(linha['estoque'])
                produtos.append(linha)
    except Exception as e:
        print(f'Erro ao carregar produtos: {e}')
        return []
    return produtos

def save_products(lista_produtos):
    os.makedirs('data', exist_ok=True)
    try:
        with open(CAMINHO_ARQUIVO_PRODUTOS, 'w', encoding='utf-8', newline='') as f:
            escritor_csv = csv.DictWriter(f, fieldnames=CABECALHO)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_produtos) 
    except Exception as e:
        print(f'Erro ao salvar produtos: {e}')

def list_products():
    produtos = load_products() 
    print("\n--- Lista de Produtos Cadastrados ---")
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return
    print(f"{'ID':<5} | {'Nome':<25} | {'Preço Venda':<15} | {'Estoque':<10}")
    print("-" * 65)
    for produto in produtos:
        preco_formatado = f"R${produto['preco_venda']:.2f}"
        print(f"{produto['id']:<5} | {produto['nome']:<25} | {preco_formatado:<15} | {produto['estoque']:<10}")

def register_products():
    print('\n--- Cadastro de Novo Produto ---')
    
    nome = obter_input_texto("Nome do produto: ")
    preco_custo = obter_input_numerico("Preço de custo (ex: 9.50): ", tipo_dado=float, permitir_zero=True)
    preco_venda = obter_input_numerico("Preço de venda (ex: 14.99): ", tipo_dado=float, permitir_zero=True)
    estoque = obter_input_numerico("Quantidade inicial em estoque: ", tipo_dado=int, permitir_zero=True)
    
    produtos = load_products()
    novo_id = max([p['id'] for p in produtos] + [0]) + 1
    
    novo_produto = {
        "id": novo_id, "nome": nome, "preco_custo": preco_custo,
        "preco_venda": preco_venda, "estoque": estoque
    }
    
    produtos.append(novo_produto)
    save_products(produtos) 
    
    print(f"\nProduto '{nome}' cadastrado com sucesso!")
    
def find_product_by_id(id_produto):
    produtos = load_products()
    return next((produto for produto in produtos if produto['id'] == id_produto), None)

def edit_products():
    print("\n--- Editar Produto ---")
    list_products()
    id_produto = obter_input_numerico("\nDigite o ID do produto que deseja editar: ")
    
    produto_to_edit = find_product_by_id(id_produto)
    if not produto_to_edit:
        print("Produto não encontrado.")
        return
    
    print(f"\nEditando produto: {produto_to_edit['nome']} (ID: {produto_to_edit['id']})")
    print("Deixe o campo em branco e pressione Enter para manter o valor atual.")
    
    novo_nome = input(f"Novo nome [{produto_to_edit['nome']}]: ").strip()
    novo_preco_venda = obter_input_numerico_opcional(f"Novo preço de venda [{produto_to_edit['preco_venda']}]: ", tipo_dado=float)
    estoque_adicional = obter_input_numerico_opcional(f"Adicionar ao estoque (Estoque atual: {produto_to_edit['estoque']}): ", tipo_dado=int)
    
    produtos = load_products()
    for p in produtos:
        if p['id'] == id_produto:
            if novo_nome: p['nome'] = novo_nome
            if novo_preco_venda is not None: p['preco_venda'] = novo_preco_venda
            if estoque_adicional is not None: p['estoque'] += estoque_adicional
            break
    
    save_products(produtos) 
    print("Produto atualizado com sucesso!")

def delete_product():
    print("\n--- Excluir Produto ---")
    list_products()
    id_to_delete = obter_input_numerico("\nDigite o ID do produto que deseja excluir: ")
    
    produto_to_delete = find_product_by_id(id_to_delete)
    if not produto_to_delete:
        print("Produto não encontrado.")
        return
    
    confirmacao = input(f"Tem certeza que deseja excluir o produto '{produto_to_delete['nome']}'? (S/N): ").upper()
    
    if confirmacao == 'S': 
        produtos = load_products()
        produtos_restantes = [p for p in produtos if p['id'] != id_to_delete]
        save_products(produtos_restantes) 
        print("Produto excluído com sucesso!")
    else:
        print("Operação de exclusão cancelada.")
        
def stock():
    print("\n--- Reposição de Estoque ---")
    list_products()
    
    id_produto = obter_input_numerico("\nDigite o ID do produto para adicionar estoque: ")
    produto_para_repor = find_product_by_id(id_produto)

    if not produto_para_repor:
        print("Produto não encontrado.")
        return
        
    quantidade = obter_input_numerico(f"Digite a quantidade a ser adicionada ao estoque de '{produto_para_repor['nome']}': ")

    produtos_atuais = load_products()
    for p in produtos_atuais:
        if p['id'] == id_produto:
            p['estoque'] += quantidade
            break
    save_products(produtos_atuais)

    lista_transacoes = transacoes.load_transactions()
    novo_id = max([t.get('id', 0) for t in lista_transacoes] + [0]) + 1
    
    nova_transacao = {
        "id": novo_id, "tipo": "compra", "produto_id": id_produto, "quantidade": quantidade,
        "valor_total": -(produto_para_repor['preco_custo'] * quantidade),
        "timestamp": datetime.now().isoformat()
    }
    lista_transacoes.append(nova_transacao)
    transacoes.save_transactions(lista_transacoes)

    print(f"{quantidade} unidades adicionadas ao estoque de '{produto_para_repor['nome']}' com sucesso!")