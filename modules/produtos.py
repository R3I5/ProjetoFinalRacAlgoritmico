import csv
import os
from datetime import datetime
from modules import transacoes

arquivo_produtos = os.path.join('data', 'produtos.csv')
cabecalho = ['id', 'nome', 'preco_custo', 'preco_venda', 'estoque']

def load_products():
    if not os.path.exists(arquivo_produtos): return []
    produtos = []
    try:
        with open(arquivo_produtos, 'r', encoding='utf-8', newline='') as f:
            leitor_csv = csv.DictReader(f)
            for linha in leitor_csv:
                linha['id'] = int(linha['id'])
                linha['preco_custo'] = float(linha['preco_custo'])
                linha['preco_venda'] = float(linha['preco_venda'])
                linha['estoque'] = int(linha['estoque'])
                produtos.append(linha)
    except Exception:
        return []
    return produtos

def save_products(lista_produtos):
    os.makedirs('data', exist_ok=True)
    try:
        with open(arquivo_produtos, 'w', encoding='utf-8', newline='') as f:
            escritor_csv = csv.DictWriter(f, fieldnames=cabecalho)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_produtos) 
    except Exception as e:
        print(f'❌ Erro ao salvar produtos: {e}')

def get_products_as_string():
    produtos = load_products()
    if not produtos:
        return "Nenhum produto cadastrado ainda."
    
    header = f"{'ID':<5} | {'Nome':<25} | {'Preço Venda':<15} | {'Estoque':<10}\n"
    separator = "-" * 65 + "\n"
    rows = ""
    for produto in produtos:
        preco_formatado = f"R${produto['preco_venda']:.2f}"
        rows += f"{produto['id']:<5} | {produto['nome']:<25} | {preco_formatado:<15} | {produto['estoque']:<10}\n"
    return header + separator + rows

def find_product_by_id(id_produto):
    return next((produto for produto in load_products() if produto['id'] == id_produto), None)

def register_product(nome, preco_custo, preco_venda, estoque):
    produtos = load_products()
    novo_id = max([p.get('id', 0) for p in produtos] + [0]) + 1
    
    novo_produto = {
        "id": novo_id, "nome": nome, "preco_custo": preco_custo,
        "preco_venda": preco_venda, "estoque": estoque
    }
    produtos.append(novo_produto)
    save_products(produtos)
    return True

def edit_product(id_produto, novo_nome, novo_preco_venda, estoque_adicional):
    produtos = load_products()
    produto_editado = False
    for p in produtos:
        if p['id'] == id_produto:
            if novo_nome: p['nome'] = novo_nome
            if novo_preco_venda is not None: p['preco_venda'] = novo_preco_venda
            if estoque_adicional is not None: p['estoque'] += estoque_adicional
            produto_editado = True
            break
    if produto_editado:
        save_products(produtos)
    return produto_editado

def delete_product(id_produto):
    produtos = load_products()
    produtos_restantes = [p for p in produtos if p['id'] != id_produto]
    if len(produtos) == len(produtos_restantes):
        return False
    save_products(produtos_restantes)
    return True

def stock(id_produto, quantidade):
    produto_para_repor = find_product_by_id(id_produto)
    if not produto_para_repor: return False

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
    return True