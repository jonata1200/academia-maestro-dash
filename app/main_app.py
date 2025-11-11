# app/main_app.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Importa a lógica que já criamos
from utils.data_handler import DataHandler
from analysis.alunos_analysis import AlunosAnalysis
from analysis.aulas_analysis import AulasAnalysis
from analysis.financeiro_analysis import FinanceiroAnalysis
from analysis.professores_analysis import ProfessoresAnalysis

# Configurações da aparência da interface
ctk.set_appearance_mode("System")  # Pode ser "Dark" ou "Light"
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO DA JANELA PRINCIPAL ---
        self.title("Academia Maestro - Dashboard")
        self.geometry("1100x780")

        # --- CARREGAMENTO DOS DADOS ---
        # A lógica de dados e análise é a mesma de antes!
        self.data_handler = DataHandler()
        self.alunos_analyser = AlunosAnalysis(self.data_handler)
        self.financeiro_analyser = FinanceiroAnalysis(self.data_handler)
        # (Você pode carregar os outros analisadores aqui quando precisar deles)

        # --- LAYOUT DA INTERFACE ---
        # Configura o grid para expandir com a janela
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- PAINEL DE NAVEGAÇÃO LATERAL (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Maestro Dash", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botões de navegação (exemplo)
        self.overview_button = ctk.CTkButton(self.sidebar_frame, text="Visão Geral", command=self.show_overview_frame)
        self.overview_button.grid(row=1, column=0, padx=20, pady=10)
        
        # --- FRAME PRINCIPAL PARA CONTEÚDO ---
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Inicializa a tela de Visão Geral
        self.show_overview_frame()

    def show_overview_frame(self):
        # Limpa o frame de conteúdo antes de desenhar novos widgets
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        # --- WIDGETS DA TELA DE VISÃO GERAL ---
        
        # 1. KPI: Total de Alunos Ativos
        total_ativos = self.alunos_analyser.get_total_alunos(status='Ativo')
        kpi_alunos_label = ctk.CTkLabel(self.main_content_frame, text=f"Alunos Ativos\n{total_ativos}", font=ctk.CTkFont(size=25, weight="bold"))
        kpi_alunos_label.pack(pady=20, padx=10, side="top", fill="x")

        # 2. Gráfico: Faturamento Mensal para 2024
        faturamento_df = self.financeiro_analyser.get_faturamento_total_por_mes('2024')
        
        # Cria a figura do Matplotlib
        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plota os dados se não estiverem vazios
        if not faturamento_df.empty:
            ax.bar(faturamento_df['mes'], faturamento_df['faturamento_mensal'], color='#1f77b4')
            ax.set_title('Faturamento Mensal em 2024')
            ax.set_ylabel('Faturamento (R$)')
            ax.tick_params(axis='x', rotation=45)
            fig.tight_layout()

        # Incorpora o gráfico na interface CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self.main_content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, pady=15, padx=10)


# --- PONTO DE ENTRADA DA APLICAÇÃO ---
if __name__ == "__main__":
    app = App()
    app.mainloop()