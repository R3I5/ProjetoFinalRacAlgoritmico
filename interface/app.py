# interface/app.py

import customtkinter as ctk
from interface.tela_login import TelaLogin
from interface.tela_principal import TelaPrincipal

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão")
        self.geometry("350x450") # Tamanho inicial para a tela de login
        self.resizable(False, False)
        self.usuario_logado = None

        self.mostrar_tela_login()

    def mostrar_tela_login(self):
        # Limpa a janela se houver algo
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("350x450")
        self.login_frame = TelaLogin(self, self.callback_apos_login)
        self.login_frame.pack(fill="both", expand=True)

    def mostrar_tela_principal(self):
        # Limpa a janela e mostra a tela principal
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("800x600")
        self.resizable(True, True)
        self.principal_frame = TelaPrincipal(self, self.usuario_logado, self.logout)
        self.principal_frame.pack(fill="both", expand=True)

    def callback_apos_login(self, usuario):
        """Função chamada pela TelaLogin após um login bem-sucedido."""
        self.usuario_logado = usuario
        self.mostrar_tela_principal()

    def logout(self):
        """Função chamada pela TelaPrincipal para fazer logout."""
        self.usuario_logado = None
        self.mostrar_tela_login()