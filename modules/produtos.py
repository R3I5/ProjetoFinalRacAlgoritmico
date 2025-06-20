import csv
import os

arquivo_produtos = os.path.join('data','produtos.csv')
cabecalho = ['id','nome','preco_custo','preco_venda','estoque']

# le o que esta presente no arquivo produtos.csv
def load_product():
    if not os.path.exists(arquivo_produtos):
        return[]
    produtos = []
    try:
        with open(arquivo_produtos, 'r', encoding='utf=8',newline='') as f:
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

# escreve sobre o arquivo products.csv
def save_product():
    os.makedirs('data',exist_ok=True)
    try:
        with open(arquivo_produtos, 'r', encoding='utf-8',newline='') as f:
            escritor_csv = csv.DictWriter(f, fieldnames=cabecalho)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_produtos)
    except Exception as e:
        print(f'Erro ao salvar produtos: {e}')
    pass

# lista os produtos 
def list_products():
    produtos = load_product()
    print("\n --- Lista de Produtos cadastrados ---")
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return
    print(f"{'ID':<5} | {'Nome':<25} | {'Preço Venda':<15} | {'Estoque':<10}")
    print("-" * 65)
    for produto in produtos:
        preco_formatado = f"R${produto['preco_venda']:.2f}"
        print(f"{produto['id']:<5} | {produto['nome']:<25} | {preco_formatado:<15} | {produto['estoque']:<10}")

# registra novos produtos
def register_products():
    pass

# edita produtos 
def edit_products():
    pass

# deleta produtos
def delete_product():
    pass