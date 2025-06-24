import customtkinter as ctk
from modules import relatorios

class TelaRelatorios(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # --- Configuração do Grid Layout ---
        self.grid_rowconfigure(1, weight=1) # A linha da caixa de texto se expande
        self.grid_columnconfigure(0, weight=1)

        # --- Frame Superior para Título e Botão ---
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(top_frame, text="Relatório de Vendas do Dia", font=ctk.CTkFont(size=16, weight="bold"))
        label.grid(row=0, column=0, sticky="w")
        
        btn_recarregar = ctk.CTkButton(top_frame, text="Recarregar Relatório", width=160, command=self.carregar_relatorio)
        btn_recarregar.grid(row=0, column=1, sticky="e")

        # --- Caixa de Texto para Exibir o Relatório ---
        self.textbox = ctk.CTkTextbox(self, font=("Courier", 13))
        self.textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Carrega o relatório ao iniciar a tela
        self.carregar_relatorio()

    def carregar_relatorio(self):
        """Busca os dados do backend e atualiza a caixa de texto."""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        
        # Chama a função "headless" do módulo de relatórios
        report_string = relatorios.get_daily_sales_report_string()
        
        self.textbox.insert("1.0", report_string)
        self.textbox.configure(state="disabled") # Bloqueia a edição pelo usuário