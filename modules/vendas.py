from datetime import datetime
from modules import produtos, transacoes

def make_sell(usuario_logado):
    print("\n Realizar Nova Venda ---")
    carrinho = []
    valor_total_venda = 0.0
    
    while True:
        produtos.list_products()
        
        try:
            id_produto = int(input("\n Digite o ID do produto para adicionar no carrinho (ou 0 para finalizar): "))
            if id_produto == 0:
                if not carrinho:
                    print("Venda cancelada.")
                    return
                break

            produto_selecionado = produtos.find_product_by_id(id_produto)
        
            if not produto_selecionado:
                print("Produto não encontrado")
                continue
        
            quantidade = int(input(f"Digite a quantidade de {produto_selecionado['nome']}: "))
            if quantidade <= 0:
                print("Quantidade deve ser positiva.")
                continue
        
            if produto_selecionado['estoque'] < quantidade:
                print(f"Estoque insuficiente! Estoque atual de {produto_selecionado['nome']}: {produto_selecionado['estoque']}.")
                continue
        
            carrinho.append({
                "produto_id": produto_selecionado['id'],
                "nome": produto_selecionado['nome'],
                "quantidade": quantidade,
                "preco_unidade": produto_selecionado['preco_venda']
            })
            valor_total_venda += produto_selecionado['preco_venda'] * quantidade
            print(f"Item adcionado! Subtotal do carrinho: R${valor_total_venda:.2f}")
        
        except ValueError:
            print("Entrada inválida. Por favor, digite números para ID e quantidade")
        
        
        