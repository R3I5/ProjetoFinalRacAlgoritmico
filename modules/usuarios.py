import json
import os
from datetime import datetime

arquivo_usuarios = os.path.join('data','usuarios.json')

#carrega a lista de usuários do arquivo usuarios.json
def load_user(): 
    if not os.path.exists(arquivo_usuarios): #verifica se o arquivo existe
        return [] #retorna uma lista vazia se o arquivo não existe
    try:
        with open(arquivo_usuarios, 'r', encoding='utf-8') as f:
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
    usuario = carregar_usuarios()
    for usuario in usuarios:
        if usuario['username'] == username and usuario['password'] == password:
            return usuario # login bem-sucedido
    return None

# cadastra um novo usuario
def register_user():
    print(f"\n --- Cadastro de Novo Usuário ---")
    usuarios = carregar_usuarios()
    
    #coleta de dados
    nome_completo = input("Digite o nome completo: ")
    username = input("Digite um nome de usuário (login): ")
    
    for u in usuarios:
        if u['username'] == username:
            print(f"Erro: O nome de usuário: '{username}' já existe. Tente outro")
            return
    
    password = input("Digite uma senha: ")
    
    #seleção de cargo
    while True:
        role = input("Digite o cargo('admin' ou 'vendedor')").lower
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
    salvar_usuarios(usuarios)
    
    print(f"\n Usuário '{username}' cadastrado com sucesso! ")