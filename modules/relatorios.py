from datetime import datetime
from modules import transacoes, usuarios

def get_daily_sales_report_string():
    lista_de_transacoes = transacoes.load_transactions()
    data_hoje = datetime.now().date()
    
    vendas_de_hoje = [t for t in lista_de_transacoes if t.get('tipo') == 'venda' and datetime.fromisoformat(t['timestamp']).date() == data_hoje]
            
    if not vendas_de_hoje:
        return "Nenhuma venda registrada hoje."

    mapa_usuarios = {u['id']: u['username'] for u in usuarios.load_user()}
    total_vendido_dia = sum(venda.get('valor_total', 0) for venda in vendas_de_hoje)
    total_lucro_dia = sum(venda.get('lucro_total', 0) for venda in vendas_de_hoje)

    relatorio_str = "--- Relatório de Vendas do Dia ---\n"
    relatorio_str += "-" * 70 + "\n"

    for venda in vendas_de_hoje:
        hora_venda = datetime.fromisoformat(venda['timestamp']).strftime('%H:%M:%S')
        nome_vendedor = mapa_usuarios.get(venda['usuario_id'], "N/A")

        relatorio_str += f"Venda ID: {venda['id']} | Horário: {hora_venda} | Vendedor: {nome_vendedor}\n"
        for item in venda['produtos_vendidos']:
            relatorio_str += f"  - {item['quantidade']}x {item['nome']} (R$ {item['preco_unidade']:.2f})\n"
        relatorio_str += f"  > Total da Venda: R$ {venda['valor_total']:.2f} | Lucro: R$ {venda['lucro_total']:.2f}\n"
        relatorio_str += "-" * 70 + "\n"
        
    relatorio_str += "\n--- Resumo do Dia ---\n"
    relatorio_str += f"Total Vendido: R$ {total_vendido_dia:.2f}\n"
    relatorio_str += f"Lucro Total do Dia: R$ {total_lucro_dia:.2f}\n"
    relatorio_str += "-" * 70 + "\n"
    
    return relatorio_str