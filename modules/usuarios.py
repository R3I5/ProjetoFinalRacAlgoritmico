# modules/usuarios.py

import json
import os
from datetime import datetime
from modules.utils import obter_input_texto, obter_input_numerico # Importando as validações

arquivo_usuarios = os.path.join('data', 'usuarios.json')

def load_user():
    if not os.path.exists(arquivo_usuarios):
        return []
    try:
        with open(arquivo_usuarios, 'r', encoding='utf-8') as f:
            content = f.read()
            return [] if not content else json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_user(lista_usuarios):
    os.makedirs('data', exist_ok=True)
    with open(arquivo_usuarios, 'w', encoding='utf-8') as f:
        json.dump(lista_usuarios, f, indent=2, ensure_ascii=False)

def validate_user(username, password):
    lista_usuarios = load_user()
    for usuario in lista_usuarios:
        if usuario['username'] == username and usuario['password'] == password:
            return usuario
    return None

def list_users():
    usuarios = load_user()
    print("\n--- Lista de Usuários do Sistema ---")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    print(f"{'ID':<5} | {'Nome Completo':<25} | {'Username':<20} | {'Cargo':<10}")
    print("-" * 70)
    for usuario in usuarios:
        print(f"{usuario['id']:<5} | {usuario['nome_completo']:<25} | {usuario['username']:<20} | {usuario['role']:<10}")

def delete_user(usuario_logado):
    print("\n--- Excluir Usuário ---")
    list_users()
    
    id_to_delete = obter_input_numerico("\nDigite o ID do usuário que deseja excluir: ")

    if id_to_delete == usuario_logado['id']:
        print("Você não pode excluir sua própria conta de administrador.")
        return

    usuarios = load_user()
    usuario_to_delete = next((u for u in usuarios if u['id'] == id_to_delete), None)

    if not usuario_to_delete:
        print("Usuário não encontrado com este ID.")
        return
    
    confirmacao = input(f"Tem certeza que deseja excluir o usuário '{usuario_to_delete['username']}'? (S/N): ").upper()
    if confirmacao == 'S':
        usuarios_restantes = [user for user in usuarios if user['id'] != id_to_delete]
        save_user(usuarios_restantes)
        print("✅ Usuário excluído com sucesso!")
    else:
        print("Operação de exclusão cancelada.")
        
def register_user(forcar_admin=False):
    print("\n--- Cadastro de Novo Usuário ---")
    usuarios = load_user()
    
    nome_completo = obter_input_texto("Digite o nome completo: ")
    
    while True:
        username = obter_input_texto("Digite um nome de usuário (login): ", permitir_espacos=False)
        if any(u['username'] == username for u in usuarios):
            print(f"Erro: O nome de usuário '{username}' já existe. Tente outro.")
        else:
            break
    
    while True:
        password = input("Digite uma senha: ").strip()
        if password:
            break
        else:
            print("Erro: A senha não pode ser vazia.")
    
    if forcar_admin:
        role = 'admin'
        print("INFO: Conta definida como Administrador.")
    else:
        while True:
            role = input("Digite o cargo ('admin' ou 'vendedor'): ").lower().strip()
            if role in ['admin', 'vendedor']:
                break
            else:
                print("Cargo inválido. Por favor, digite 'admin' ou 'vendedor'.")
            
    novo_id = max([u['id'] for u in usuarios] + [0]) + 1
    
    novo_usuario = {
        "id": novo_id, "nome_completo": nome_completo, "username": username,
        "password": password, "role": role, "data_criacao": datetime.now().isoformat()
    }
    
    usuarios.append(novo_usuario)
    save_user(usuarios)
    
    print(f"\nUsuário '{username}' cadastrado com sucesso!")