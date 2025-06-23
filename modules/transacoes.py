import json
import os

arquivo_transacoes = os.path.join('data','transacoes.json')

def load_transactions():
    if not os.path.exists(arquivo_transacoes):
        return []
    try:
        with open(arquivo_transacoes, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
def save_transactions(lista_transacoes):
    os.makedirs('data', exist_ok=True)
    with open(arquivo_transacoes, 'w', encoding='utf-8') as f:
        json.dump(lista_transacoes, f, indent=2, ensure_ascii=False)