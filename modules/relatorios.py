# modules/relatorios.py

from datetime import datetime
from modules import transacoes, usuarios, produtos

def relatorio_vendas_diarias():
    print("\n--- Relatório de Vendas do Dia ---")
    
    lista_de_transacoes = transacoes.load_transactions()
    data_hoje = datetime.now().date()
    
    vendas_de_hoje = [t for t in lista_de_transacoes if t.get('tipo') == 'venda' and datetime.fromisoformat(t['timestamp']).date() == data_hoje]
            
    if not vendas_de_hoje:
        print("Nenhuma venda registrada hoje."); return

    # Otimização: Carrega os usuários uma vez e cria um mapa para busca rápida
    mapa_usuarios = {u['id']: u['username'] for u in usuarios.load_user()}
    
    total_vendido_dia = sum(venda.get('valor_total', 0) for venda in vendas_de_hoje)
    total_lucro_dia = sum(venda.get('lucro_total', 0) for venda in vendas_de_hoje)

    print("-" * 70)
    for venda in vendas_de_hoje:
        hora_venda = datetime.fromisoformat(venda['timestamp']).strftime('%H:%M:%S')
        nome_vendedor = mapa_usuarios.get(venda['usuario_id'], "N/A")

        print(f"Venda ID: {venda['id']} | Horário: {hora_venda} | Vendedor: {nome_vendedor}")
        for item in venda['produtos_vendidos']:
            print(f"  - {item['quantidade']}x {item['nome']} (R$ {item['preco_unidade']:.2f})")
        print("-" * 70)
        
    print("\n--- Resumo do Dia ---")
    print(f"Total Vendido: R$ {total_vendido_dia:.2f}")
    print(f"Lucro Total do Dia: R$ {total_lucro_dia:.2f}")
    print("-" * 70)