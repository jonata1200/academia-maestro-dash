# ui/overview_view.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# (A função create_kpi_card pode ser mantida como está)
def create_kpi_card(master, title, value, icon):
    card = ctk.CTkFrame(master, corner_radius=10, fg_color="#F5F5F5")
    card_icon = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=30))
    card_icon.pack(pady=(10, 0))
    card_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14))
    card_title.pack()
    card_value = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=22, weight="bold"))
    card_value.pack(pady=(0, 10))
    return card

class OverviewView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        
        title_label = ctk.CTkLabel(self, text="Visão Geral do Negócio", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        kpi_container.pack(fill="x", padx=10, pady=10)
        kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        total_ativos = analyzers["alunos"].get_total_alunos(status='Ativo')
        faturamento_ano = analyzers["financeiro"].get_faturamento_total_por_mes('2024')['faturamento_mensal'].sum()
        aulas_concluidas = analyzers["aulas"].get_total_aulas_por_status('2024').query("status == 'Concluída'")['total_aulas'].sum()

        card1 = create_kpi_card(kpi_container, "Total de Alunos Ativos", str(total_ativos), "👥")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        card2 = create_kpi_card(kpi_container, "Faturamento Anual (2024)", f"R$ {faturamento_ano:,.2f}", "💰")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        card3 = create_kpi_card(kpi_container, "Aulas Concluídas (2024)", str(aulas_concluidas), "🎶")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        tab_view = ctk.CTkTabview(self, height=500, fg_color="#F5F5F5")
        tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        tab_faturamento = tab_view.add("Evolução Mensal")
        tab_instrumentos = tab_view.add("Popularidade de Instrumentos")

        # Gráfico 1: Faturamento Mensal
        faturamento_df = analyzers["financeiro"].get_faturamento_total_por_mes('2024')
        fig1 = Figure(figsize=(10, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.bar(faturamento_df['mes'], faturamento_df['faturamento_mensal'], color='#1A3A7D') # COR ATUALIZADA
        ax1.set_title('Evolução do Faturamento em 2024', color='black') # COR ATUALIZADA
        ax1.set_ylabel('Valor (R$)', color='black') # COR ATUALIZADA
        ax1.tick_params(axis='x', colors='black') # COR ATUALIZADA
        ax1.tick_params(axis='y', colors='black') # COR ATUALIZADA
        fig1.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, master=tab_faturamento)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Gráfico 2: Popularidade
        popularidade_df = analyzers["aulas"].get_popularidade_instrumentos()
        fig2 = Figure(figsize=(10, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(popularidade_df['nome_instrumento'], popularidade_df['total_aulas_agendadas'], color='#2E7D32') # NOVA COR
        ax2.set_title('Aulas por Instrumento', color='black') # COR ATUALIZADA
        ax2.set_ylabel('Nº de Aulas Agendadas', color='black') # COR ATUALIZADA
        ax2.tick_params(axis='x', colors='black') # COR ATUALIZADA
        ax2.tick_params(axis='y', colors='black') # COR ATUALIZADA
        fig2.tight_layout()

        canvas2 = FigureCanvasTkAgg(fig2, master=tab_instrumentos)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="top", fill="both", expand=True)