# ui/overview_view.py
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_kpi_card(master, title, value, icon):
    # ... (código existente)
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
        self.analyzers = analyzers
        self.data_handler = data_handler
        
        title_label = ctk.CTkLabel(self, text="Visão Geral do Negócio", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        self.kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_container.pack(fill="x", padx=10, pady=10)
        self.kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        self.tab_view = ctk.CTkTabview(self, height=500, fg_color="#F5F5F5")
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        self.tab_faturamento = self.tab_view.add("Evolução Mensal")
        self.tab_instrumentos = self.tab_view.add("Popularidade de Instrumentos")

    def update_view(self, start_date, end_date):
        for widget in self.kpi_container.winfo_children(): widget.destroy()

        total_ativos = self.analyzers["alunos"].get_total_alunos(status='Ativo')
        df_faturamento = self.analyzers["financeiro"].get_faturamento_total_por_mes(start_date, end_date)
        faturamento_periodo = df_faturamento['faturamento_mensal'].sum()
        df_aulas = self.analyzers["aulas"].get_total_aulas_por_status(start_date, end_date)
        aulas_concluidas = df_aulas.query("status == 'Concluída'")['total_aulas'].sum()

        create_kpi_card(self.kpi_container, "Total de Alunos Ativos", str(total_ativos), "👥").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        create_kpi_card(self.kpi_container, "Faturamento no Período", f"R$ {faturamento_periodo:,.2f}", "💰").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        create_kpi_card(self.kpi_container, "Aulas Concluídas no Período", str(aulas_concluidas), "🎶").grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.update_tabs_content(start_date, end_date, df_faturamento)

    def update_tabs_content(self, start_date, end_date, df_faturamento):
        for tab in [self.tab_faturamento, self.tab_instrumentos]:
            for widget in tab.winfo_children(): widget.destroy()
        
        # Gráfico 1: Faturamento Mensal
        fig1 = Figure(figsize=(10, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.bar(df_faturamento['mes'], df_faturamento['faturamento_mensal'], color='#1A3A7D')
        ax1.set_title('Evolução do Faturamento no Período', color='black')
        ax1.set_ylabel('Valor (R$)', color='black')
        ax1.tick_params(axis='x', colors='black', rotation=45)
        ax1.tick_params(axis='y', colors='black')
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=self.tab_faturamento)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Gráfico 2: Popularidade
        popularidade_df = self.analyzers["aulas"].get_popularidade_instrumentos(start_date, end_date)
        fig2 = Figure(figsize=(10, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(popularidade_df['nome_instrumento'], popularidade_df['total_aulas_agendadas'], color='#2E7D32')
        ax2.set_title('Aulas por Instrumento no Período', color='black')
        ax2.set_ylabel('Nº de Aulas Agendadas', color='black')
        ax2.tick_params(axis='x', colors='black', rotation=45)
        ax2.tick_params(axis='y', colors='black')
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=self.tab_instrumentos)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)