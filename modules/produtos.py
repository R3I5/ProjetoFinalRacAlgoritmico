import csv
import os

arquivo_produtos = os.path.join('data', 'produtos.csv')
CABECALHO = ['id', 'nome', 'preco_custo', 'preco_venda', 'estoque']


def load_products():
    if not os.path.exists(arquivo_produtos):
        return []
    
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
    except Exception as e:
        print(f'Erro ao carregar produtos: {e}')
        return []
    return produtos


def save_products(lista_produtos):
    os.makedirs('data', exist_ok=True)
    try:
        
        with open(arquivo_produtos, 'w', encoding='utf-8', newline='') as f:
            escritor_csv = csv.DictWriter(f, fieldnames=CABECALHO)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_produtos) 
    except Exception as e:
        print(f' Erro ao salvar produtos: {e}')


def list_products():
    produtos = load_products() 
    print("\n--- Lista de Produtos Cadastrados ---")
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return
    print(f"{'ID':<5} | {'Nome':<25} | {'Preço Venda':<15} | {'Estoque':<10}")
    print("-" * 65)
    for produto in produtos:
        preco_formatado = f"R${produto['preco_venda']:.2f}"
        print(f"{produto['id']:<5} | {produto['nome']:<25} | {preco_formatado:<15} | {produto['estoque']:<10}")


def register_products():
    print('\n--- Cadastro de Novo Produto ---')
    
    try: 
        nome = input("Nome do produto: ")
        preco_custo = float(input("Preço de custo (ex: 9.50): "))
        preco_venda = float(input("Preço de venda (ex: 14.99): "))
        estoque = int(input("Quantidade inicial em estoque: "))
    except ValueError: 
        print("Erro: Valor inválido inserido. Operação cancelada.")
        return
    
    produtos = load_products()
    novo_id = max([p['id'] for p in produtos] + [0]) + 1
    
    novo_produto = {
        "id": novo_id, "nome": nome, "preco_custo": preco_custo,
        "preco_venda": preco_venda, "estoque": estoque
    }
    
    produtos.append(novo_produto)
    save_products(produtos) 
    
    print(f"\n Produto '{nome}' cadastrado com sucesso!")
    
def find_product_by_id(id_produto):
    produtos = load_products()
    for produto in produtos:
        if produto['id'] == id_produto:
            return produto
    return None


def edit_products():
    print("\n--- Editar Produto ---")
    list_products()
    
    try:
        id_produto = int(input("\nDigite o ID do produto que deseja editar: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return
    
    produto_to_edit = find_product_by_id(id_produto)
    
    if not produto_to_edit:
        print("Produto não encontrado.")
        return
    
    print(f"\nEditando produto: {produto_to_edit['nome']} (ID: {produto_to_edit['id']})")
    print("Deixe o campo em branco e pressione Enter para manter o valor atual.")
    
    try: 
        novo_nome = input(f"Novo nome [{produto_to_edit['nome']}]: ")
        novo_preco_venda = input(f"Novo preço de venda [{produto_to_edit['preco_venda']}]: ")
        estoque_adicional = input(f"Adicionar ao estoque (Estoque atual: {produto_to_edit['estoque']}): ")
        
        produtos = load_products()
        for p in produtos:
            if p['id'] == id_produto:
                if novo_nome:
                    p['nome'] = novo_nome
                if novo_preco_venda:
                    p['preco_venda'] = float(novo_preco_venda)
                if estoque_adicional:
                    p['estoque'] += int(estoque_adicional)
                break
            
        save_products(produtos) 
        print("Produto atualizado com sucesso!")
        
    except ValueError:
        print("Erro: Valor numérico inválido. Nenhuma alteração foi salva.")


def delete_product():
    print("\n--- Excluir Produto ---")
    list_products()
    
    try:
        id_to_delete = int(input("\nDigite o ID do produto que deseja excluir: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return
    
    produto_to_delete = find_product_by_id(id_to_delete)
    
    if not produto_to_delete:
        print("Produto não encontrado.")
        return
    
    confirmacao = input(f"Tem certeza que deseja excluir o produto '{produto_to_delete['nome']}'? (S/N): ").upper()
    
    if confirmacao == 'S': 
        produtos = load_products()
        produtos_restantes = [p for p in produtos if p['id'] != id_to_delete]
        save_products(produtos_restantes) 
        print("Produto excluído com sucesso!")
    else:
        print("Operação de exclusão cancelada.")