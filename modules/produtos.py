import csv
import os
from datetime import datetime
from modules import transacoes

# --- Caminho e Cabeçalho do Arquivo ---
arquivo_produtos = os.path.join('data', 'produtos.csv')
cabecalho = ['id', 'nome', 'preco_custo', 'preco_venda', 'estoque']


def load_products():
    """Carrega todos os produtos do arquivo CSV."""
    if not os.path.exists(arquivo_produtos):
        return []
    
    produtos = []
    try:
        with open(arquivo_produtos, 'r', encoding='utf-8', newline='') as f:
            leitor_csv = csv.DictReader(f)
            for linha in leitor_csv:
                # Converte os tipos de dados para os formatos corretos
                linha['id'] = int(linha['id'])
                linha['preco_custo'] = float(linha['preco_custo'])
                linha['preco_venda'] = float(linha['preco_venda'])
                linha['estoque'] = int(linha['estoque'])
                produtos.append(linha)
    except Exception:
        # Retorna lista vazia em caso de erro de leitura ou arquivo corrompido
        return []
    return produtos


def save_products(lista_produtos):
    """Salva a lista completa de produtos no arquivo CSV."""
    os.makedirs('data', exist_ok=True)
    try:
        with open(arquivo_produtos, 'w', encoding='utf-8', newline='') as f:
            escritor_csv = csv.DictWriter(f, fieldnames=cabecalho)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_produtos) 
    except Exception as e:
        print(f'❌ Erro ao salvar produtos: {e}')


def get_products_as_string():
    """Retorna uma string formatada com a lista de produtos para exibição."""
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
    """Encontra e retorna um único produto pelo seu ID."""
    return next((produto for produto in load_products() if produto['id'] == id_produto), None)


def register_product(nome, preco_custo, preco_venda, estoque):
    """Cadastra um novo produto após validar os preços."""
    # Garante que o preço de venda é maior que o de custo.
    if preco_venda <= preco_custo:
        return False # A mensagem de LOG foi removida daqui

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
    """Edita um produto existente, validando a alteração de preço."""
    produtos = load_products()
    produto_editado = False
    for p in produtos:
        if p['id'] == id_produto:
            # Se um novo preço de venda foi fornecido, valida-o contra o preço de custo.
            if novo_preco_venda is not None:
                if novo_preco_venda <= p['preco_custo']:
                    return False # A mensagem de LOG foi removida daqui
                p['preco_venda'] = novo_preco_venda

            if novo_nome: 
                p['nome'] = novo_nome
            if estoque_adicional is not None: 
                p['estoque'] += estoque_adicional
            
            produto_editado = True
            break
            
    if produto_editado:
        save_products(produtos)
        
    return produto_editado


def delete_product(id_produto):
    """Exclui um produto da lista."""
    produtos = load_products()
    produtos_restantes = [p for p in produtos if p['id'] != id_produto]
    if len(produtos) == len(produtos_restantes):
        return False # Produto não encontrado
    save_products(produtos_restantes)
    return True


def stock(id_produto, quantidade):
    """Adiciona estoque a um produto e registra como uma transação de 'compra'."""
    produto_para_repor = find_product_by_id(id_produto)
    if not produto_para_repor: 
        return False

    # Atualiza o estoque na lista de produtos
    produtos_atuais = load_products()
    for p in produtos_atuais:
        if p['id'] == id_produto:
            p['estoque'] += quantidade
            break
    save_products(produtos_atuais)

    # Cria a transação de compra (despesa)
    lista_transacoes = transacoes.load_transactions()
    novo_id = max([t.get('id', 0) for t in lista_transacoes] + [0]) + 1
    nova_transacao = {
        "id": novo_id, 
        "tipo": "compra", 
        "produto_id": id_produto, 
        "quantidade": quantidade,
        "valor_total": -(produto_para_repor['preco_custo'] * quantidade), # Valor negativo pois é uma saída
        "timestamp": datetime.now().isoformat()
    }
    lista_transacoes.append(nova_transacao)
    transacoes.save_transactions(lista_transacoes)
    return True