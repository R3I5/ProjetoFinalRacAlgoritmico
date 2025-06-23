# run_gui.py

from interface.app import App
from modules import usuarios

if __name__ == "__main__":
    # A lógica de verificação de primeiro usuário continua aqui, no console, por simplicidade.
    lista_de_usuarios = usuarios.load_user()
    if not lista_de_usuarios:
        print("--- Configuração Inicial do Sistema (via console) ---")
        print("Nenhum usuário encontrado. Vamos criar a conta do administrador.")
        # Como as funções de input foram removidas do backend, chamamos uma função
        # que ainda usa o console para o primeiro setup.
        usuarios.setup_initial_admin()
        print("\n✅ Administrador configurado! Execute o programa novamente para usar a interface.")
    else:
        # Se já existem usuários, inicia a aplicação gráfica
        app = App()
        app.mainloop()