import customtkinter as ctk
from tkinter import messagebox, simpledialog
from modules import produtos

class TelaProdutos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # --- Configuração do Grid Layout ---
        self.grid_columnconfigure(1, weight=1) # A coluna da lista se expande
        self.grid_rowconfigure(0, weight=1)

        # --- Frame dos Botões de Ação (Coluna 0) ---
        action_frame = ctk.CTkFrame(self, width=150)
        action_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        action_frame.grid_rowconfigure(5, weight=1) # Espaço flexível para empurrar os botões para cima

        ctk.CTkLabel(action_frame, text="Ações de Produto", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(action_frame, text="Cadastrar", command=self.cadastrar_produto).grid(row=1, column=0, padx=10, pady=7, sticky="ew")
        ctk.CTkButton(action_frame, text="Editar", command=self.editar_produto).grid(row=2, column=0, padx=10, pady=7, sticky="ew")
        ctk.CTkButton(action_frame, text="Excluir", command=self.excluir_produto, fg_color="#D32F2F", hover_color="#B71C1C").grid(row=3, column=0, padx=10, pady=7, sticky="ew")
        ctk.CTkButton(action_frame, text="Repor Estoque", command=self.repor_estoque).grid(row=4, column=0, padx=10, pady=7, sticky="ew")

        # --- Frame da Lista de Produtos (Coluna 1) ---
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        
        ctk.CTkLabel(list_frame, text="Lista de Produtos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10,5))
        self.textbox = ctk.CTkTextbox(list_frame, font=("Courier", 13))
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(0,10))
        
        self.atualizar_lista()

    def atualizar_lista(self):
        """Busca os dados do backend e atualiza a caixa de texto."""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        lista_str = produtos.get_products_as_string()
        self.textbox.insert("1.0", lista_str)
        self.textbox.configure(state="disabled")

    def cadastrar_produto(self):
        """Abre janelas de diálogo para cadastrar um novo produto."""
        try:
            nome = simpledialog.askstring("Cadastro", "Nome do produto:", parent=self)
            if not nome: return

            preco_custo = float(simpledialog.askstring("Cadastro", "Preço de custo (ex: 9.50):", parent=self))
            preco_venda = float(simpledialog.askstring("Cadastro", "Preço de venda (ex: 14.99):", parent=self))
            estoque = int(simpledialog.askstring("Cadastro", "Estoque inicial:", parent=self))
            
            if preco_custo < 0 or preco_venda < 0 or estoque < 0:
                messagebox.showerror("Erro de Validação", "Valores numéricos não podem ser negativos.", parent=self)
                return

            if produtos.register_product(nome, preco_custo, preco_venda, estoque):
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!", parent=self)
                self.atualizar_lista()
            else:
                messagebox.showerror("Erro", "Não foi possível cadastrar o produto.", parent=self)

        except (ValueError, TypeError):
            messagebox.showerror("Erro de Validação", "Por favor, insira valores numéricos válidos para preços e estoque.", parent=self)

    def editar_produto(self):
        """Abre janelas de diálogo para editar um produto existente."""
        try:
            id_prod_str = simpledialog.askstring("Editar", "Digite o ID do produto a editar:", parent=self)
            if not id_prod_str: return
            id_prod = int(id_prod_str)

            prod_existente = produtos.find_product_by_id(id_prod)
            if not prod_existente:
                messagebox.showerror("Erro", "Produto não encontrado.", parent=self)
                return

            novo_nome = simpledialog.askstring("Editar", "Novo nome (deixe em branco para manter):", initialvalue=prod_existente['nome'], parent=self)
            novo_preco_str = simpledialog.askstring("Editar", "Novo preço de venda (deixe em branco para manter):", initialvalue=str(prod_existente['preco_venda']), parent=self)
            
            novo_preco = float(novo_preco_str) if novo_preco_str else None

            if produtos.edit_product(id_prod, novo_nome, novo_preco, None): # Estoque é editado em outra função
                messagebox.showinfo("Sucesso", "Produto editado com sucesso!", parent=self)
                self.atualizar_lista()
            else:
                messagebox.showerror("Erro", "Não foi possível editar o produto.", parent=self)

        except (ValueError, TypeError):
            messagebox.showerror("Erro de Validação", "Valores inválidos.", parent=self)

    def excluir_produto(self):
        """Pede um ID e confirma a exclusão de um produto."""
        try:
            id_prod_str = simpledialog.askstring("Excluir", "Digite o ID do produto a excluir:", parent=self)
            if not id_prod_str: return
            id_prod = int(id_prod_str)

            prod_existente = produtos.find_product_by_id(id_prod)
            if not prod_existente:
                messagebox.showerror("Erro", "Produto não encontrado.", parent=self)
                return
            
            if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir '{prod_existente['nome']}'?", parent=self):
                if produtos.delete_product(id_prod):
                    messagebox.showinfo("Sucesso", "Produto excluído.", parent=self)
                    self.atualizar_lista()
                else:
                    messagebox.showerror("Erro", "Falha ao excluir o produto.", parent=self)
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "ID inválido.", parent=self)

    def repor_estoque(self):
        """Pede ID e quantidade para repor o estoque de um produto."""
        try:
            id_prod_str = simpledialog.askstring("Repor Estoque", "Digite o ID do produto:", parent=self)
            if not id_prod_str: return
            id_prod = int(id_prod_str)
            
            prod_existente = produtos.find_product_by_id(id_prod)
            if not prod_existente:
                messagebox.showerror("Erro", "Produto não encontrado.", parent=self)
                return

            qtd_str = simpledialog.askstring("Repor Estoque", f"Quantidade a adicionar ao estoque de '{prod_existente['nome']}':", parent=self)
            if not qtd_str: return
            qtd = int(qtd_str)
            
            if qtd > 0:
                if produtos.stock(id_prod, qtd):
                    messagebox.showinfo("Sucesso", "Estoque atualizado.", parent=self)
                    self.atualizar_lista()
                else:
                    messagebox.showerror("Erro", "Não foi possível atualizar o estoque.", parent=self)
            else:
                messagebox.showwarning("Aviso", "A quantidade deve ser positiva.", parent=self)
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Valores inválidos.", parent=self)