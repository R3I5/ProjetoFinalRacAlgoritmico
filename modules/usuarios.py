# modules/usuarios.py
import json
import os
from datetime import datetime

arquivo_usuarios = os.path.join('data', 'usuarios.json')

# --- Funções de Load/Save (sem alteração) ---
def load_user():
    if not os.path.exists(arquivo_usuarios): return []
    try:
        with open(arquivo_usuarios, 'r', encoding='utf-8') as f:
            content = f.read()
            return [] if not content else json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError): return []

def save_user(lista_usuarios):
    os.makedirs('data', exist_ok=True)
    with open(arquivo_usuarios, 'w', encoding='utf-8') as f:
        json.dump(lista_usuarios, f, indent=2, ensure_ascii=False)

# --- Funções de Lógica "Headless" ---
def validate_user(username, password):
    for usuario in load_user():
        if usuario['username'] == username and usuario['password'] == password:
            return usuario
    return None

def get_all_users():
    return load_user()

def find_user_by_id(user_id):
    for user in load_user():
        if user['id'] == user_id:
            return user
    return None

def register_user(nome_completo, username, password, role):
    usuarios = load_user()
    if any(u['username'] == username for u in usuarios):
        return None # Usuário já existe
    
    novo_id = max([u.get('id', 0) for u in usuarios] + [0]) + 1
    novo_usuario = {
        "id": novo_id, "nome_completo": nome_completo, "username": username,
        "password": password, "role": role, "data_criacao": datetime.now().isoformat()
    }
    usuarios.append(novo_usuario)
    save_user(usuarios)
    return novo_usuario

def delete_user_by_id(id_to_delete):
    usuarios = load_user()
    usuarios_restantes = [user for user in usuarios if user['id'] != id_to_delete]
    if len(usuarios) == len(usuarios_restantes):
        return False # Nenhum usuário foi deletado
    save_user(usuarios_restantes)
    return True

# --- Função Especial para Setup Inicial ---
def setup_initial_admin():
    """Usa console APENAS para criar o primeiro admin."""
    print("\n--- Cadastro do Administrador Inicial ---")
    nome_completo = input("Digite o nome completo do admin: ")
    username = input("Digite um nome de usuário (login) para o admin: ")
    password = input("Digite uma senha para o admin: ")
    register_user(nome_completo, username, password, role='admin')
    
# Adicione esta função em modules/usuarios.py

def get_users_as_string():
    """Retorna a lista de usuários como uma única string formatada para a GUI."""
    usuarios = load_user()
    if not usuarios:
        return "Nenhum usuário cadastrado."

    header = f"{'ID':<5} | {'Nome Completo':<25} | {'Username':<20} | {'Cargo':<10}\n"
    separator = "-" * 70 + "\n"
    rows = ""
    for usuario in usuarios:
        rows += f"{usuario['id']:<5} | {usuario['nome_completo']:<25} | {usuario['username']:<20} | {usuario['role']:<10}\n"
    
    return header + separator + rows