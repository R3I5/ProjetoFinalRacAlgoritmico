from modules import usuarios, produtos

def menu_admin(usuario_logado):
    while True:
        print(f"\n--- Menu Principal (Admin: {usuario_logado['nome_completo']})---")
        print("--- Vendas ---")
        print("1. Realizar Venda")
        print("--- Produtos ---")
        print("2. Listar Produtos")
        print("3. Cadastrar Produtos")
        print("4. Editar Produtos")
        print("5. Excluir Produtos")
        print("--- Usuários ---")
        print("6. Cadastrar Novo Usuário")
        print("7. Listar Usuários")
        print("8. Excluir Usuário")
        print("--- Sistema ---")
        print("0. Sair (Logout)")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            #produtos.listProtudos
            pass
        elif opcao == '2':
            #produtos.registerProdutos
            pass
        elif opcao == '3':
            #produtos.sell
            pass
        elif opcao == '4':
            #produtos.edit
            pass
        elif opcao == '5':
            #list.UserW
            pass
        elif opcao == '6':
            usuarios.register_user()
            pass
        elif opcao == '7':
            usuarios.list_users()
            pass
        elif opcao == '8':
            usuarios.delete_user(usuario_logado)
            pass
        elif opcao == '0':
            print("Fazendo Logout...")
            break
        else:
            print("Opção Inválida!")
            
            
def menu_vendedor(usuario_logado):
    while True:
        print(f"\n--- Menu Principal (Vendedor: {usuario_logado['nome_completo']})---")
        print("1. Listar Produtos")
        print("2. Vender Produtos")


def main():
        
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
        menu_admin(usuario_logado)
        pass
    elif usuario_logado['role'] == 'vendedor':
        menu_vendedor(usuario_logado)
        pass
    
if __name__ == "__main__":
    main()