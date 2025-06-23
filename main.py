# main.py

from modules import usuarios, produtos, vendas, relatorios, utils

def menu_admin(usuario_logado):
    while True:
        print(f"\n--- Menu Principal (Admin: {usuario_logado['nome_completo']}) ---")
        print("\n--- Vendas ---")
        print("1. Realizar Venda")
        print("\n--- Produtos ---")
        print("2. Listar Produtos")
        print("3. Cadastrar Produto")
        print("4. Editar Produto")
        print("5. Excluir Produto")
        print("6. Repor Estoque")
        print("\n--- Usuários e Relatórios ---")
        print("7. Cadastrar Novo Usuário")
        print("8. Listar Usuários")
        print("9. Excluir Usuário")
        print("10. Relatório de Vendas do Dia")
        print("\n--- Sistema ---")
        print("0. Sair (Logout)")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1': vendas.make_sell(usuario_logado)
        elif opcao == '2': produtos.list_products()
        elif opcao == '3': produtos.register_products()
        elif opcao == '4': produtos.edit_products()
        elif opcao == '5': produtos.delete_product()
        elif opcao == '6': produtos.stock()
        elif opcao == '7': usuarios.register_user()
        elif opcao == '8': usuarios.list_users()
        elif opcao == '9': usuarios.delete_user(usuario_logado)
        elif opcao == '10': relatorios.relatorio_vendas_diarias()
        elif opcao == '0': print("\nFazendo Logout..."); break
        else: print("Opção Inválida!")
            
def menu_vendedor(usuario_logado):
    while True:
        print(f"\n--- Menu Principal (Vendedor: {usuario_logado['nome_completo']})---")
        print("1. Realizar Venda")
        print("2. Listar Produtos")
        print("0. Sair (Logout)")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1': vendas.make_sell(usuario_logado)
        elif opcao == '2': produtos.list_products()
        elif opcao == '0': print("\nFazendo logout..."); break
        else: print("Opção inválida")

def main():
    lista_de_usuarios = usuarios.load_user()
    if not lista_de_usuarios:
        print("--- Configuração Inicial do Sistema ---")
        print("Nenhum usuário encontrado. Vamos criar a conta do administrador.")
        usuarios.register_user(forcar_admin=True)
        print(f"\nAdministrador configurado com sucesso! Por favor, faça o login.")
        print("-" * 40)
        
    usuario_logado = None
    while not usuario_logado:
        print(f"\n--- Tela de Login ---")
        username = input("Usuário: ")
        password = input("Senha: ")
        
        usuario_logado = usuarios.validate_user(username,password)
        
        if not usuario_logado:
            print("Usuário ou senha incorretos. Tente novamente.")
        else:
            print(f"Login bem-sucedido! Bem-vindo(a), {usuario_logado['nome_completo']}!")
        
    if usuario_logado['role'] == 'admin':
        menu_admin(usuario_logado)
    elif usuario_logado['role'] == 'vendedor':
        menu_vendedor(usuario_logado)
    
if __name__ == "__main__":
    main()