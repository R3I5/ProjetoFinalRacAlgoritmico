from datetime import datetime
from modules import produtos, transacoes

def process_sale(carrinho, usuario_logado):
    if not carrinho:
        return False, "Carrinho vazio."

    lista_produtos_atual = produtos.load_products()
    
    for item_carrinho in carrinho:
        for produto_db in lista_produtos_atual:
            if produto_db['id'] == item_carrinho['produto_id']:
                if produto_db['estoque'] < item_carrinho['quantidade']:
                    return False, f"Estoque insuficiente para {produto_db['nome']}."
                break
    
    lucro_total_venda = 0.0
    valor_total_venda = 0.0

    for item_carrinho in carrinho:
        for produto_db in lista_produtos_atual:
            if produto_db['id'] == item_carrinho['produto_id']:
                produto_db['estoque'] -= item_carrinho['quantidade']
                valor_item = produto_db['preco_venda'] * item_carrinho['quantidade']
                lucro_item = (produto_db['preco_venda'] - produto_db['preco_custo']) * item_carrinho['quantidade']
                
                valor_total_venda += valor_item
                lucro_total_venda += lucro_item
                break
    
    produtos.save_products(lista_produtos_atual)

    lista_transacoes_atual = transacoes.load_transactions()
    novo_id_transacao = max([t.get('id', 0) for t in lista_transacoes_atual] + [0]) + 1
    
    nova_transacao = {
        "id": novo_id_transacao, "tipo": "venda", "produtos_vendidos": carrinho, 
        "valor_total": round(valor_total_venda, 2), "lucro_total": round(lucro_total_venda, 2),
        "usuario_id": usuario_logado['id'], "timestamp": datetime.now().isoformat()
    }
    
    lista_transacoes_atual.append(nova_transacao)
    transacoes.save_transactions(lista_transacoes_atual)
    
    return True, "Venda realizada com sucesso!"