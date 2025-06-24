import customtkinter as ctk
from tkinter import messagebox
from .tela_produtos import TelaProdutos
from .tela_usuarios import TelaUsuarios
from .tela_vendas import TelaVenda
from .tela_relatorios import TelaRelatorios

class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, callback_logout):
        super().__init__(master)
        self.usuario_logado = usuario_logado
        self.callback_logout = callback_logout

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(top_frame, text=f"Usuário: {self.usuario_logado['nome_completo']} ({self.usuario_logado['role']})", font=("Arial", 16)).pack(side="left")
        ctk.CTkButton(top_frame, text="Logout", width=100, command=self.callback_logout).pack(side="right")
        
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(fill="both", expand=True, padx=20, pady=20)
        action_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(action_frame, text="Menu de Opções", font=("Arial", 14, "bold")).pack(pady=(0, 10))

        ctk.CTkButton(action_frame, text="Realizar Venda", height=40, command=self.abrir_tela_venda).pack(fill="x", pady=5)
        
        if self.usuario_logado['role'] == 'admin':
            ctk.CTkButton(action_frame, text="Gerenciar Produtos", height=40, command=self.abrir_tela_produtos).pack(fill="x", pady=5)
            ctk.CTkButton(action_frame, text="Gerenciar Usuários", height=40, command=self.abrir_tela_usuarios).pack(fill="x", pady=5)
            ctk.CTkButton(action_frame, text="Ver Relatórios", height=40, command=self.abrir_tela_relatorios).pack(fill="x", pady=5)

    def abrir_tela_produtos(self):
        if not hasattr(self, 'janela_produtos') or not self.janela_produtos.winfo_exists():
            self.janela_produtos = TelaProdutos(self)
            self.janela_produtos.grab_set()
        else:
            self.janela_produtos.lift()

    def abrir_tela_venda(self):
        if not hasattr(self, 'janela_venda') or not self.janela_venda.winfo_exists():
            self.janela_venda = TelaVenda(self, self.usuario_logado)
            self.janela_venda.grab_set()
        else:
            self.janela_venda.lift()
            
    def abrir_tela_usuarios(self):
        if not hasattr(self, 'janela_usuarios') or not self.janela_usuarios.winfo_exists():
            self.janela_usuarios = TelaUsuarios(self)
            self.janela_usuarios.grab_set()
        else:
            self.janela_usuarios.lift()

    def abrir_tela_relatorios(self):
        if not hasattr(self, 'janela_relatorios') or not self.janela_relatorios.winfo_exists():
            self.janela_relatorios = TelaRelatorios(self)
            self.janela_relatorios.grab_set()
        else:
            self.janela_relatorios.lift()