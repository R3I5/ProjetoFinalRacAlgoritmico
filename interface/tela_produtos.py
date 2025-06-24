# interface/tela_produtos.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from modules import produtos

class TelaProdutos(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gerenciamento de Produtos")
        self.geometry("750x500")

        # --- Frame dos Botões de Ação ---
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkButton(action_frame, text="Cadastrar Produto", command=self.cadastrar_produto).pack(fill="x", pady=5)
        ctk.CTkButton(action_frame, text="Editar Produto", command=self.editar_produto).pack(fill="x", pady=5)
        ctk.CTkButton(action_frame, text="Excluir Produto", command=self.excluir_produto).pack(fill="x", pady=5)
        ctk.CTkButton(action_frame, text="Repor Estoque", command=self.repor_estoque).pack(fill="x", pady=5)

        # --- Frame da Lista de Produtos ---
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="Lista de Produtos", font=("Arial", 16)).pack()
        self.textbox = ctk.CTkTextbox(list_frame, font=("monospace", 12))
        self.textbox.pack(fill="both", expand=True)
        
        self.atualizar_lista()

    def atualizar_lista(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        lista_str = produtos.get_products_as_string()
        self.textbox.insert("1.0", lista_str)
        self.textbox.configure(state="disabled")

    def cadastrar_produto(self):
        dialog = ctk.CTkInputDialog(text="Digite o nome do novo produto:", title="Cadastrar Produto")
        nome = dialog.get_input()
        if not nome: return
        
        try:
            preco_custo = float(simpledialog.askstring("Cadastro", "Digite o preço de custo:", parent=self))
            preco_venda = float(simpledialog.askstring("Cadastro", "Digite o preço de venda:", parent=self))
            estoque = int(simpledialog.askstring("Cadastro", "Digite o estoque inicial:", parent=self))
            
            if preco_custo < 0 or preco_venda < 0 or estoque < 0:
                messagebox.showerror("Erro", "Valores não podem ser negativos.", parent=self)
                return

            produtos.register_product(nome, preco_custo, preco_venda, estoque)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!", parent=self)
            self.atualizar_lista()
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Valores numéricos inválidos inseridos.", parent=self)

    def editar_produto(self):
        try:
            id_prod = int(simpledialog.askstring("Editar", "Digite o ID do produto a editar:", parent=self))
            prod_existente = produtos.find_product_by_id(id_prod)
            if not prod_existente:
                messagebox.showerror("Erro", "Produto não encontrado.", parent=self)
                return

            nome = simpledialog.askstring("Editar", "Novo nome (deixe em branco para manter):", initialvalue=prod_existente['nome'], parent=self)
            preco = simpledialog.askstring("Editar", "Novo preço de venda (deixe em branco para manter):", initialvalue=str(prod_existente['preco_venda']), parent=self)
            
            produtos.edit_product(id_prod, nome, float(preco) if preco else None, None)
            messagebox.showinfo("Sucesso", "Produto editado!", parent=self)
            self.atualizar_lista()
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Valores inválidos.", parent=self)

    def excluir_produto(self):
        try:
            id_prod = int(simpledialog.askstring("Excluir", "Digite o ID do produto a excluir:", parent=self))
            prod_existente = produtos.find_product_by_id(id_prod)
            if not prod_existente:
                messagebox.showerror("Erro", "Produto não encontrado.", parent=self)
                return
            
            if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir '{prod_existente['nome']}'?", parent=self):
                if produtos.delete_product(id_prod):
                    messagebox.showinfo("Sucesso", "Produto excluído.", parent=self)
                    self.atualizar_lista()
                else:
                    messagebox.showerror("Erro", "Produto não encontrado ao tentar deletar.", parent=self)
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "ID inválido.", parent=self)

    def repor_estoque(self):
        try:
            id_prod = int(simpledialog.askstring("Repor Estoque", "Digite o ID do produto:", parent=self))
            prod_existente = produtos.find_product_by_id(id_prod)
            if not prod_existente:
                messagebox.showerror("Erro", "Produto não encontrado.", parent=self)
                return

            qtd = int(simpledialog.askstring("Repor Estoque", f"Quantidade a adicionar ao estoque de '{prod_existente['nome']}'", parent=self))
            if qtd > 0:
                produtos.stock(id_prod, qtd)
                messagebox.showinfo("Sucesso", "Estoque atualizado.", parent=self)
                self.atualizar_lista()
            else:
                messagebox.showwarning("Aviso", "A quantidade deve ser positiva.", parent=self)
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Valores inválidos.", parent=self)