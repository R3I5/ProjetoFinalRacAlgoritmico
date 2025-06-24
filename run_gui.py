# run_gui.py
from interface.app import App
from modules import usuarios

if __name__ == "__main__":
    lista_de_usuarios= usuarios.load_user()
    if not lista_de_usuarios:
        print("--- Configuração Inicial do Sistema (via console) ---")
        print("Nenhum usuário encontrado. Vamos criar a conta do administrador.")
        usuarios.setup_initial_admin() # Função especial que ainda usa console
        print("\n✅ Administrador configurado! Execute o programa novamente para usar a interface.")
    else:
        app = App()
        app.mainloop()