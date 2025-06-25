import customtkinter as ctk
from tkinter import messagebox, simpledialog
from modules import usuarios

class TelaUsuarios(ctk.CTkFrame):
    def __init__(self, master, usuario_logado):
        super().__init__(master)
        self.usuario_logado = usuario_logado # Essencial para a verificação de autoexclusão

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        action_frame = ctk.CTkFrame(self, width=150)
        action_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        action_frame.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(action_frame, text="Ações de Usuário", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(action_frame, text="Cadastrar Usuário", command=self.cadastrar_usuario).grid(row=1, column=0, padx=10, pady=7, sticky="ew")
        ctk.CTkButton(action_frame, text="Excluir Usuário", command=self.excluir_usuario, fg_color="#D32F2F", hover_color="#B71C1C").grid(row=2, column=0, padx=10, pady=7, sticky="ew")

        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        
        ctk.CTkLabel(list_frame, text="Lista de Usuários do Sistema", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10,5))
        self.textbox = ctk.CTkTextbox(list_frame, font=("Courier", 12))
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(0,10))
        
        self.atualizar_lista()

    def atualizar_lista(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        lista_str = usuarios.get_users_as_string()
        self.textbox.insert("1.0", lista_str)
        self.textbox.configure(state="disabled")

    def cadastrar_usuario(self):
        nome = simpledialog.askstring("Cadastro", "Nome Completo:", parent=self)
        if not nome or not nome.strip(): return
        
        username = simpledialog.askstring("Cadastro", "Nome de Usuário (login):", parent=self)
        if not username or not username.strip(): return

        password = simpledialog.askstring("Cadastro", "Senha:", show='*', parent=self)
        if not password or not password.strip(): return

        role = simpledialog.askstring("Cadastro", "Cargo (admin ou vendedor):", parent=self)
        if not role or role.strip().lower() not in ['admin', 'vendedor']:
            messagebox.showerror("Erro de Validação", "Cargo inválido. Use 'admin' ou 'vendedor'.", parent=self)
            return

        novo_usuario = usuarios.register_user(nome.strip(), username.strip(), password, role.strip().lower())
        
        if novo_usuario:
            messagebox.showinfo("Sucesso", f"Usuário '{username}' cadastrado com sucesso!", parent=self)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", f"O nome de usuário '{username}' já existe.", parent=self)

    def excluir_usuario(self):
        try:
            id_user_str = simpledialog.askstring("Excluir", "Digite o ID do usuário a excluir:", parent=self)
            if not id_user_str: return
            id_user = int(id_user_str)

            if id_user == self.usuario_logado['id']:
                messagebox.showwarning("Ação Ilegal", "Você não pode excluir a sua própria conta.", parent=self)
                return

            usuario_existente = usuarios.find_user_by_id(id_user)
            if not usuario_existente:
                messagebox.showerror("Erro", "Usuário não encontrado.", parent=self)
                return
            
            if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o usuário '{usuario_existente['username']}'?", parent=self):
                if usuarios.delete_user_by_id(id_user):
                    messagebox.showinfo("Sucesso", "Usuário excluído.", parent=self)
                    self.atualizar_lista()
                else:
                    messagebox.showerror("Erro", "Falha ao excluir o usuário.", parent=self)
        except (ValueError, TypeError):
            messagebox.showerror("Erro de Validação", "ID inválido. Por favor, digite um número.", parent=self)