import customtkinter as ctk
from modules import relatorios

class TelaRelatorios(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Relatórios")
        self.geometry("700x500")

        ctk.CTkLabel(self, text="Relatório de Vendas do Dia", font=("Arial", 16)).pack(pady=10)

        textbox = ctk.CTkTextbox(self, width=680, height=450, font=("monospace", 12))
        textbox.pack(pady=10, padx=10)

        # Pega o relatório como string e insere na caixa de texto
        report_string = relatorios.get_daily_sales_report_string()
        textbox.insert("1.0", report_string)
        textbox.configure(state="disabled") # Bloqueia a edição