from modules import usuarios, produtos

def main():
    # função que inicia e gerencia o programa
    
    # verificação de primeira execução
    lista_de_usuarios = usuarios.load_user()
    if not lista_de_usuarios:
        print("--- Configuração Inicial do Sistema ---")
        print("Nenhum usuário encontrado. Vamos criar a conta do administrador")
        usuarios.register_user(forcar_admin=True)
        print(f"\n Administrador configurado com sucesso! Por favor, faça o login")
        print("-" * 40)
        
    # loop de login principal
    usuario_logado = None
    while not usuario_logado:
        print(f"\n --- Tela de Login ---")
        username = input("Usuário: ")
        password = input("Senha: ")
        
        usuario_logado = usuarios.validate_user(username,password)
        
        if not usuario_logado:
            print("Usuario ou senha incorretos. Tente novamente")
        else:
            print(f"Login bem-sucedido! Bem-vindo(a), {usuario_logado['nome_completo']}!")
        
    if usuario_logado['role'] == 'admin':
        # menu_admin(usuario_logado)
        pass
    elif usuario_logado['role'] == 'vendedor':
        #menu_vendedor(usuario_logado)
        pass
    
if __name__ == "__main__":
    main()