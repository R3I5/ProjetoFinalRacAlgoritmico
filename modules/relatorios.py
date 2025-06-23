from datetime import datetime
from modules import transacoes, usuarios, produtos

def relatorio_vendas_diarias():
    """
    Carrega as transações e gera um relatório formatado das vendas
    realizadas no dia de hoje (data atual).
    """
    print("\n--- Relatório de Vendas do Dia ---")
    
    lista_de_transacoes = transacoes.load_transactions()
    
    # Pega a data de hoje, sem as horas
    data_hoje = datetime.now().date()
    
    vendas_de_hoje = []
    for t in lista_de_transacoes:
        # Converte a data da transação (que é uma string) para um objeto de data
        data_transacao = datetime.fromisoformat(t['timestamp']).date()
        if t['tipo'] == 'venda' and data_transacao == data_hoje:
            vendas_de_hoje.append(t)
            
    if not vendas_de_hoje:
        print("Nenhuma venda registrada hoje.")
        return

    total_vendido_dia = 0.0
    total_lucro_dia = 0.0

    print("-" * 70)
    for venda in vendas_de_hoje:
        # Para cada venda, vamos mostrar os detalhes
        total_vendido_dia += venda['valor_total']
        total_lucro_dia += venda['lucro_total']
        hora_venda = datetime.fromisoformat(venda['timestamp']).strftime('%H:%M:%S')
        
        # Busca o nome do vendedor para exibir no relatório
        vendedor = usuarios.load_user() # Simplificado, ideal seria uma função find_user_by_id
        nome_vendedor = "N/A"
        for u in vendedor:
            if u['id'] == venda['usuario_id']:
                nome_vendedor = u['username']
                break

        print(f"Venda ID: {venda['id']} | Horário: {hora_venda} | Vendedor: {nome_vendedor}")
        for item in venda['produtos_vendidos']:
            print(f"  - {item['quantidade']}x {item['nome']} (R$ {item['preco_unidade']:.2f})")
        print("-" * 70)
        
    print("\n--- Resumo do Dia ---")
    print(f"Total Vendido: R$ {total_vendido_dia:.2f}")
    print(f"Lucro Total do Dia: R$ {total_lucro_dia:.2f}")
    print("-" * 70)