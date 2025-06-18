import json
import os
from datetime import datetime

arquivo_usuarios = os.path.join('data','usuarios.json')

#carrega a lista de usuários do arquivo usuarios.json
def load_user(): 
    if not os.path.exists(arquivo_usuarios): #verifica se o arquivo existe
        return [] #retorna uma lista vazia se o arquivo não existe
    try:
        with open(arquivo_usuarios, 'r', encoding='utf-8') as f: #'r' abre o arquivo como 'read' encoding garante padrões de linguagem e f determina um nome para o arquivo aberto
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return [] # retorna lista vazia se o arquivo está vazio ou corrompido

#salva a lista de usuários de volta no arquivo usuarios.json
def save_user(lista_usuarios): 
    os.makedirs('data',exist_ok=True) #garante que a pasta data exista
    with open(arquivo_usuarios, 'w', encoding='utf-8') as f: 
        json.dump(lista_usuarios, f, indent=2, ensure_ascii=False)
    return

# valida as credenciais de um usuario, retorna o dicionario do usuario se for valido
def validate_user(username,password): 
    lista_usuarios = load_user()
    for usuario in lista_usuarios:
        if usuario['username'] == username and usuario['password'] == password:
            return usuario # login bem-sucedido
    return None

def list_users():
    usuarios = load_user()
    print(f"\n --- Lista de Usuários do Sistema ---")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    print(f"{'ID':<5} | {'Nome Completo':<25} | {'Username':<20} | {'Cargo':<10}")
    print("-" * 70)
    for usuario in usuarios:
        print(f"{usuario['id']:<5} | {usuario['nome_completo']:<25} | {usuario['username']:<20} | {usuario['role']:<10}")

def delete_user(usuario_logado):
    print(f"\n --- Excluir Usuário ---")
    list_users()
    try:
        id_to_delete = int(input(f"\n Digite o ID do usuário que deseja excluir: "))
    except ValueError:
        print("ID inválido. Por favor, digite um número.")
        return
    
    if id_to_delete == usuario_logado['id']:
        print("Você não pode excluir sua própria conta de administrador. ")
        return
    
    usuarios = load_user()
    usuario_to_delete = None
    for u in usuarios:
        if u['id'] == id_to_delete:
            usuario_to_delete = u
            break
    if not usuario_to_delete:
        print("Usuário não encontrado com este ID")
        return
    
    confirmacao = input(f"Tem certeza que deseja excluir o usuário {usuario_to_delete['username']}? Esta ação é permanente. (S/N): ").upper()
    if confirmacao == 'S':
        # CORREÇÃO 3: A lógica da lista foi corrigida para filtrar corretamente
        usuarios_restantes = [user for user in usuarios if user['id'] != id_to_delete]
        save_user(usuarios_restantes)
        print("Usuário excluído com sucesso!")
    else:
        print("Operação de exclusão cancelada.")
        
# cadastra um novo usuario
def register_user(forcar_admin=False):
    print(f"\n --- Cadastro de Novo Usuário ---")
    usuarios = load_user()
    
    #coleta de dados
    nome_completo = input("Digite o nome completo: ")
    username = input("Digite um nome de usuário (login): ")
    
    for u in usuarios:
        if u['username'] == username:
            print(f"Erro: O nome de usuário: '{username}' já existe. Tente outro")
            return
    
    password = input("Digite uma senha: ")
    
    #seleção de cargo
    if forcar_admin:
        role = 'admin'
        print("INFO: Conta definida como Admininstrador")
    else:
        while True:
            role = input("Digite o cargo('admin' ou 'vendedor')").lower()
            if role in ['admin','vendedor']:
                break
            else:
                print("Cargo inválido. Por favor, digite 'admin', ou 'vendedor' .")
            
            
    # criação do novo usuário
    novo_id = max([u['id'] for u in usuarios] + [0]) + 1 #gera um novo id
    
    novo_usuario = {
        "id": novo_id,
        "nome_completo": nome_completo,
        "username": username,
        "password": password,
        "role": role,
        "data_criacao": datetime.now().isoformat()        
    }
    
    usuarios.append(novo_usuario)
    save_user(usuarios)
    
    print(f"\n Usuário '{username}' cadastrado com sucesso! ")