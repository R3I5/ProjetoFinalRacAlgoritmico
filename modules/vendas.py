from datetime import datetime
from modules import produtos, transacoes

def make_sell(usuario_logado):
    """
    Gerencia o processo completo de uma venda, incluindo o cálculo de lucro,
    a atualização do estoque e o registro da transação.
    """
    print("\n--- Realizar Nova Venda ---")
    carrinho = []
    valor_total_venda = 0.0
    
    while True:
        produtos.list_products()
        
        try:
            id_produto = int(input("\nDigite o ID do produto para adicionar no carrinho (ou 0 para finalizar): "))
            if id_produto == 0:
                if not carrinho:
                    print("Venda cancelada.")
                    return
                break

            produto_selecionado = produtos.find_product_by_id(id_produto)
        
            if not produto_selecionado:
                print(" Produto não encontrado")
                continue
        
            quantidade = int(input(f"Digite a quantidade de {produto_selecionado['nome']}: "))
            if quantidade <= 0:
                print(" Quantidade deve ser positiva.")
                continue
        
            if produto_selecionado['estoque'] < quantidade:
                print(f" Estoque insuficiente! Estoque atual de {produto_selecionado['nome']}: {produto_selecionado['estoque']}.")
                continue
        
            carrinho.append({
                "produto_id": produto_selecionado['id'],
                "nome": produto_selecionado['nome'],
                "quantidade": quantidade,
                "preco_unidade": produto_selecionado['preco_venda']
            })
            valor_total_venda += produto_selecionado['preco_venda'] * quantidade
            print(f"✅ Item adicionado! Subtotal do carrinho: R${valor_total_venda:.2f}")
        
        except ValueError:
            print(" Entrada inválida. Por favor, digite números para ID e quantidade")
        
    print("\n--- Resumo da Venda ---")
    for item in carrinho:
        print(f"- {item['quantidade']}x {item['nome']} (R${item['preco_unidade']:.2f} cada)")
    print("-" * 25)
    print(f"VALOR TOTAL: R${valor_total_venda:.2f}")

    confirmacao = input("Confirmar a venda? (S/N): ").upper()

    if confirmacao != 'S':
        print("Venda cancelada pelo usuário.")
        return

    # --- LÓGICA DO LUCRO E ESTOQUE IMPLEMENTADA AQUI ---
    lista_produtos_atual = produtos.load_products()
    lucro_total_venda = 0.0  # <<-- NOVO: Inicializa a variável do lucro

    for item_carrinho in carrinho:
        for produto_db in lista_produtos_atual:
            if produto_db['id'] == item_carrinho['produto_id']:
                # 1. Atualiza o estoque (como já fazia)
                produto_db['estoque'] -= item_carrinho['quantidade']
                # 2. <<-- NOVO: Calcula o lucro deste item e soma ao total
                lucro_item = (produto_db['preco_venda'] - produto_db['preco_custo']) * item_carrinho['quantidade']
                lucro_total_venda += lucro_item
                break
                
    produtos.save_products(lista_produtos_atual)

    # --- REGISTRO DA TRANSAÇÃO COM O CAMPO DE LUCRO ---
    lista_transacoes_atual = transacoes.load_transactions()
    novo_id_transacao = max([t['id'] for t in lista_transacoes_atual] + [0]) + 1
    
    nova_transacao = {
        "id": novo_id_transacao,
        "tipo": "venda",
        "produtos_vendidos": carrinho, 
        "valor_total": valor_total_venda,
        "lucro_total": round(lucro_total_venda, 2), # <<-- NOVO: Adiciona o lucro total à transação
        "usuario_id": usuario_logado['id'],
        "timestamp": datetime.now().isoformat()
    }
    
    lista_transacoes_atual.append(nova_transacao)
    transacoes.save_transactions(lista_transacoes_atual)
    
    print("\n Venda realizada com sucesso!")