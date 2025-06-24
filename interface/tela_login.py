import customtkinter as ctk
from tkinter import messagebox
from modules import usuarios

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, callback_apos_login):
        super().__init__(master)
        self.callback_apos_login = callback_apos_login
        
        # Layout para centralizar
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        center_frame = ctk.CTkFrame(self)
        center_frame.grid()

        ctk.CTkLabel(center_frame, text="Login do Sistema", font=("Arial", 20, "bold")).pack(pady=20, padx=40)
        self.username_entry = ctk.CTkEntry(center_frame, placeholder_text="Usuário", width=200)
        self.username_entry.pack(pady=10)
        self.password_entry = ctk.CTkEntry(center_frame, placeholder_text="Senha", show="*", width=200)
        self.password_entry.pack(pady=10)
        ctk.CTkButton(center_frame, text="Entrar", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        usuario = usuarios.validate_user(username, password)

        if usuario:
            self.callback_apos_login(usuario)
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")