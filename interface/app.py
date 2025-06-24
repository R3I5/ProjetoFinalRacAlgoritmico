import customtkinter as ctk
from .tela_login import TelaLogin
from .tela_principal import TelaPrincipal

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão")
        self.usuario_logado = None
        self._frame_atual = None
        self.mostrar_tela("login")

    def mostrar_tela(self, nome_da_tela):
        if self._frame_atual:
            self._frame_atual.destroy()

        if nome_da_tela == "login":
            self.geometry("350x450")
            self.resizable(False, False)
            self._frame_atual = TelaLogin(self, self.callback_apos_login)
            self._frame_atual.pack(fill="both", expand=True)
        
        elif nome_da_tela == "principal":
            # Tamanho maior para acomodar o layout com sidebar
            self.geometry("1200x720")
            self.resizable(True, True)
            self._frame_atual = TelaPrincipal(self, self.usuario_logado, self.logout)
            self._frame_atual.pack(fill="both", expand=True)

    def callback_apos_login(self, usuario):
        self.usuario_logado = usuario
        self.mostrar_tela("principal")

    def logout(self):
        self.usuario_logado = None
        self.mostrar_tela("login")