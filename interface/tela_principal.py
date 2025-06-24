import customtkinter as ctk
from .tela_produtos import TelaProdutos
from .tela_usuarios import TelaUsuarios
from .tela_vendas import TelaVenda
from .tela_relatorios import TelaRelatorios

class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, callback_logout):
        super().__init__(master)
        self.usuario_logado = usuario_logado
        self.callback_logout = callback_logout

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        logo_label = ctk.CTkLabel(self.sidebar_frame, text="Gestão da Loja", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        ctk.CTkButton(self.sidebar_frame, text="Realizar Venda", height=40, command=self.abrir_tela_venda).grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        if self.usuario_logado['role'] == 'admin':
            ctk.CTkButton(self.sidebar_frame, text="Gerenciar Produtos", height=40, command=self.abrir_tela_produtos).grid(row=2, column=0, padx=20, pady=10, sticky="ew")
            ctk.CTkButton(self.sidebar_frame, text="Gerenciar Usuários", height=40, command=self.abrir_tela_usuarios).grid(row=3, column=0, padx=20, pady=10, sticky="ew")
            ctk.CTkButton(self.sidebar_frame, text="Relatórios", height=40, command=self.abrir_tela_relatorios).grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.callback_logout).grid(row=7, column=0, padx=20, pady=20, sticky="s")
        
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.welcome_label = ctk.CTkLabel(self.main_content_frame, text="Selecione uma opção no menu lateral para começar.", font=("Arial", 18))
        self.welcome_label.pack(pady=100)
    
    def limpar_e_mostrar_frame(self, FrameClasse):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()
        
        if FrameClasse in [TelaUsuarios, TelaVenda]:
            frame = FrameClasse(self.main_content_frame, self.usuario_logado)
        else:
            frame = FrameClasse(self.main_content_frame)
        frame.pack(fill="both", expand=True)

    def abrir_tela_produtos(self): self.limpar_e_mostrar_frame(TelaProdutos)
    def abrir_tela_usuarios(self): self.limpar_e_mostrar_frame(TelaUsuarios)
    def abrir_tela_relatorios(self): self.limpar_e_mostrar_frame(TelaRelatorios)
    def abrir_tela_venda(self): self.limpar_e_mostrar_frame(TelaVenda)