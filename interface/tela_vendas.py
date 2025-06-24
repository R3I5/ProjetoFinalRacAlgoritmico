import customtkinter as ctk
from tkinter import messagebox, simpledialog
from modules import produtos, vendas

class TelaVenda(ctk.CTkToplevel):
    def __init__(self, master, usuario_logado):
        super().__init__(master)
        self.title("Realizar Venda")
        self.geometry("900x600")
        
        self.usuario_logado = usuario_logado
        self.carrinho = []

        # --- Frame Principal ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Coluna da Esquerda (Produtos) ---
        produtos_frame = ctk.CTkFrame(main_frame)
        produtos_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        ctk.CTkLabel(produtos_frame, text="Produtos Disponíveis").pack()
        self.produtos_textbox = ctk.CTkTextbox(produtos_frame, font=("monospace", 11))
        self.produtos_textbox.pack(fill="both", expand=True)
        self.atualizar_lista_produtos()
        
        ctk.CTkButton(produtos_frame, text="Adicionar Produto ao Carrinho", command=self.adicionar_ao_carrinho).pack(pady=5)

        # --- Coluna da Direita (Carrinho) ---
        carrinho_frame = ctk.CTkFrame(main_frame)
        carrinho_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        ctk.CTkLabel(carrinho_frame, text="Carrinho de Compras").pack()
        self.carrinho_textbox = ctk.CTkTextbox(carrinho_frame, font=("monospace", 11))
        self.carrinho_textbox.pack(fill="both", expand=True)
        
        self.total_label = ctk.CTkLabel(carrinho_frame, text="Total: R$ 0.00", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=5)

        ctk.CTkButton(carrinho_frame, text="Finalizar Venda", command=self.finalizar_venda, fg_color="green", hover_color="darkgreen").pack(pady=5)

    def atualizar_lista_produtos(self):
        self.produtos_textbox.configure(state="normal")
        self.produtos_textbox.delete("1.0", "end")
        lista_str = produtos.get_products_as_string()
        self.produtos_textbox.insert("1.0", lista_str)
        self.produtos_textbox.configure(state="disabled")

    def atualizar_display_carrinho(self):
        self.carrinho_textbox.configure(state="normal")
        self.carrinho_textbox.delete("1.0", "end")
        valor_total = 0
        if not self.carrinho:
            self.carrinho_textbox.insert("1.0", "Carrinho vazio.")
        else:
            for item in self.carrinho:
                subtotal = item['quantidade'] * item['preco_unidade']
                self.carrinho_textbox.insert("end", f"{item['quantidade']}x {item['nome']} - R$ {subtotal:.2f}\n")
                valor_total += subtotal
        
        self.total_label.configure(text=f"Total: R$ {valor_total:.2f}")
        self.carrinho_textbox.configure(state="disabled")

    def adicionar_ao_carrinho(self):
        try:
            id_prod = int(simpledialog.askstring("Adicionar", "Digite o ID do produto:", parent=self))
            produto_selecionado = produtos.find_product_by_id(id_prod)
            if not produto_selecionado:
                messagebox.showerror("Erro", "Produto não encontrado.", parent=self)
                return

            qtd = int(simpledialog.askstring("Adicionar", f"Quantidade de '{produto_selecionado['nome']}':", parent=self))
            if qtd <= 0:
                messagebox.showwarning("Aviso", "Quantidade deve ser positiva.", parent=self)
                return
            if produto_selecionado['estoque'] < qtd:
                messagebox.showerror("Erro", "Estoque insuficiente.", parent=self)
                return
            
            # Adiciona ao carrinho
            self.carrinho.append({
                "produto_id": id_prod, "nome": produto_selecionado['nome'],
                "quantidade": qtd, "preco_unidade": produto_selecionado['preco_venda']
            })
            self.atualizar_display_carrinho()
            
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Entrada inválida.", parent=self)

    def finalizar_venda(self):
        if not self.carrinho:
            messagebox.showwarning("Aviso", "O carrinho está vazio.", parent=self)
            return
            
        if messagebox.askyesno("Confirmação", "Deseja finalizar a venda?", parent=self):
            sucesso, mensagem = vendas.process_sale(self.carrinho, self.usuario_logado)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem, parent=self)
                self.destroy() # Fecha a janela de venda
            else:
                messagebox.showerror("Erro na Venda", mensagem, parent=self)