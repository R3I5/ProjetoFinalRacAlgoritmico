import customtkinter as ctk
from tkinter import messagebox, simpledialog
from modules import produtos, vendas

class TelaVenda(ctk.CTkFrame):
    def __init__(self, master, usuario_logado):
        super().__init__(master)
        self.usuario_logado = usuario_logado
        self.carrinho = []

        # --- Layout Principal ---
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Coluna da Esquerda (Produtos) ---
        produtos_frame = ctk.CTkFrame(self)
        produtos_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        # --- AJUSTE 1: Configurando as colunas INTERNAS deste frame ---
        produtos_frame.grid_columnconfigure((0, 1), weight=1)
        produtos_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(produtos_frame, text="Produtos Disponíveis", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        
        self.produtos_textbox = ctk.CTkTextbox(produtos_frame, font=("Courier", 13))
        self.produtos_textbox.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.id_entry = ctk.CTkEntry(produtos_frame, placeholder_text="ID do Produto")
        self.id_entry.grid(row=2, column=0, padx=(5,2), pady=10, sticky="ew")
        
        self.qtd_entry = ctk.CTkEntry(produtos_frame, placeholder_text="Quantidade")
        self.qtd_entry.grid(row=2, column=1, padx=(2,5), pady=10, sticky="ew")

        # --- AJUSTE 2: Garantindo que o botão também se expanda ---
        ctk.CTkButton(produtos_frame, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # --- Coluna da Direita (Carrinho) ---
        carrinho_frame = ctk.CTkFrame(self)
        carrinho_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        carrinho_frame.grid_rowconfigure(1, weight=1)
        carrinho_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(carrinho_frame, text="Carrinho de Compras", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, pady=5)
        
        self.carrinho_scroll_frame = ctk.CTkScrollableFrame(carrinho_frame, label_text="Itens")
        self.carrinho_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.carrinho_scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.total_label = ctk.CTkLabel(carrinho_frame, text="Total: R$ 0.00", font=ctk.CTkFont(size=16, weight="bold"))
        self.total_label.grid(row=2, column=0, pady=5, sticky="ew")

        ctk.CTkButton(carrinho_frame, text="Finalizar Venda", command=self.finalizar_venda, fg_color="green", hover_color="darkgreen").grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        # Carrega os dados iniciais
        self.atualizar_lista_produtos()
        self.atualizar_display_carrinho()

    def atualizar_lista_produtos(self):
        self.produtos_textbox.configure(state="normal")
        self.produtos_textbox.delete("1.0", "end")
        lista_str = produtos.get_products_as_string()
        self.produtos_textbox.insert("1.0", lista_str)
        self.produtos_textbox.configure(state="disabled")

    def atualizar_display_carrinho(self):
        for widget in self.carrinho_scroll_frame.winfo_children():
            widget.destroy()

        valor_total = 0
        if not self.carrinho:
            ctk.CTkLabel(self.carrinho_scroll_frame, text="Carrinho vazio.").pack(anchor="w", padx=5)
        else:
            for i, item in enumerate(self.carrinho):
                subtotal = item['quantidade'] * item['preco_unidade']
                item_frame = ctk.CTkFrame(self.carrinho_scroll_frame, fg_color="transparent")
                item_frame.pack(fill="x", pady=2)
                item_frame.grid_columnconfigure(0, weight=1) # Faz o label ocupar o espaço
                
                label_text = f"{item['quantidade']}x {item['nome']} - R$ {subtotal:.2f}"
                ctk.CTkLabel(item_frame, text=label_text).grid(row=0, column=0, padx=5, sticky="w")
                
                btn_remover = ctk.CTkButton(item_frame, text="X", width=25, height=25, fg_color="red", hover_color="darkred",
                                            command=lambda item_index=i: self.remover_do_carrinho(item_index))
                btn_remover.grid(row=0, column=1, padx=5)
                valor_total += subtotal
        
        self.total_label.configure(text=f"Total: R$ {valor_total:.2f}")

    def remover_do_carrinho(self, item_index):
        self.carrinho.pop(item_index)
        self.atualizar_display_carrinho()

    def adicionar_ao_carrinho(self):
        try:
            id_prod_str = self.id_entry.get()
            qtd_str = self.qtd_entry.get()

            if not id_prod_str or not qtd_str:
                messagebox.showerror("Erro", "Preencha os campos de ID e Quantidade.", parent=self)
                return

            id_prod = int(id_prod_str)
            qtd = int(qtd_str)
            
            produto_selecionado = produtos.find_product_by_id(id_prod)
            if not produto_selecionado:
                messagebox.showerror("Erro", "Produto não encontrado.", parent=self)
                return
            if qtd <= 0:
                messagebox.showwarning("Aviso", "Quantidade deve ser positiva.", parent=self)
                return
            if produto_selecionado['estoque'] < qtd:
                messagebox.showerror("Erro", "Estoque insuficiente.", parent=self)
                return
            
            self.carrinho.append({
                "produto_id": id_prod, "nome": produto_selecionado['nome'],
                "quantidade": qtd, "preco_unidade": produto_selecionado['preco_venda']
            })
            self.atualizar_display_carrinho()
            self.id_entry.delete(0, 'end')
            self.qtd_entry.delete(0, 'end')

        except (ValueError, TypeError):
            messagebox.showerror("Erro de Validação", "Entrada inválida. Por favor, digite um número.", parent=self)

    def finalizar_venda(self):
        if not self.carrinho:
            messagebox.showwarning("Aviso", "O carrinho está vazio.", parent=self)
            return
            
        if messagebox.askyesno("Confirmação", f"Finalizar a venda no valor de {self.total_label.cget('text')}?", parent=self):
            sucesso, mensagem = vendas.process_sale(self.carrinho, self.usuario_logado)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem, parent=self)
                self.carrinho = []
                self.atualizar_display_carrinho()
                self.atualizar_lista_produtos()
            else:
                messagebox.showerror("Erro na Venda", mensagem, parent=self)