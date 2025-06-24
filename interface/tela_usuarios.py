import customtkinter as ctk
from tkinter import messagebox, simpledialog
from modules import usuarios

class TelaUsuarios(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gerenciamento de Usuários")
        self.geometry("700x500")

        # --- Frame dos Botões de Ação ---
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkButton(action_frame, text="Cadastrar Usuário", command=self.cadastrar_usuario).pack(fill="x", pady=5)
        ctk.CTkButton(action_frame, text="Excluir Usuário", command=self.excluir_usuario).pack(fill="x", pady=5)

        # --- Frame da Lista de Usuários ---
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="Lista de Usuários", font=("Arial", 16)).pack()
        self.textbox = ctk.CTkTextbox(list_frame, font=("monospace", 12))
        self.textbox.pack(fill="both", expand=True)
        
        self.atualizar_lista()

    def atualizar_lista(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        lista_str = usuarios.get_users_as_string()
        self.textbox.insert("1.0", lista_str)
        self.textbox.configure(state="disabled")

    def cadastrar_usuario(self):
        # Usando simpledialog para coletar os dados
        nome = simpledialog.askstring("Cadastro", "Nome Completo:", parent=self)
        if not nome: return
        
        username = simpledialog.askstring("Cadastro", "Nome de Usuário (login):", parent=self)
        if not username: return

        password = simpledialog.askstring("Cadastro", "Senha:", show='*', parent=self)
        if not password: return

        role = simpledialog.askstring("Cadastro", "Cargo (admin ou vendedor):", parent=self)
        if not role or role.lower() not in ['admin', 'vendedor']:
            messagebox.showerror("Erro", "Cargo inválido. Use 'admin' ou 'vendedor'.", parent=self)
            return

        # Chama a função do backend
        novo_usuario = usuarios.register_user(nome, username, password, role.lower())
        if novo_usuario:
            messagebox.showinfo("Sucesso", f"Usuário '{username}' cadastrado com sucesso!", parent=self)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", f"O nome de usuário '{username}' já existe.", parent=self)

    def excluir_usuario(self):
        try:
            id_user = int(simpledialog.askstring("Excluir", "Digite o ID do usuário a excluir:", parent=self))
            usuario_existente = usuarios.find_user_by_id(id_user)
            
            if not usuario_existente:
                messagebox.showerror("Erro", "Usuário não encontrado.", parent=self)
                return
            
            if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir '{usuario_existente['username']}'?", parent=self):
                if usuarios.delete_user_by_id(id_user):
                    messagebox.showinfo("Sucesso", "Usuário excluído.", parent=self)
                    self.atualizar_lista()
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o usuário.", parent=self)
        except (ValueError, TypeError):
             messagebox.showerror("Erro", "ID inválido.", parent=self)