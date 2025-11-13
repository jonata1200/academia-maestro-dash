# ui/teachers_view.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TeachersView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        
        title_label = ctk.CTkLabel(self, text="Dashboard de Professores", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        kpi_container.pack(fill="x", padx=10, pady=10)
        kpi_container.grid_columnconfigure((0, 1), weight=1)

        total_prof = len(data_handler.get_data('professores').query("status == 'Ativo'"))
        df_aulas = analyzers["aulas"].get_aulas_por_professor('2024')
        media_aulas = df_aulas['aulas_concluidas'].mean()

        ctk.CTkLabel(kpi_container, text=f"Professores Ativos\n{total_prof}", font=ctk.CTkFont(size=20)).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(kpi_container, text=f"Média de Aulas Concluídas (2024)\n{media_aulas:.1f}", font=ctk.CTkFont(size=20)).grid(row=0, column=1, padx=10, sticky="ew")

        tab_view = ctk.CTkTabview(self, height=500)
        tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        tab_aulas = tab_view.add("Aulas por Professor")
        tab_faturamento = tab_view.add("Faturamento por Professor")

        # Gráfico 1: Aulas por Professor
        fig1 = Figure(figsize=(10, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.bar(df_aulas['nome_professor'], df_aulas['aulas_concluidas'], color='#ff7f0e')
        ax1.set_title('Aulas Concluídas por Professor em 2024')
        ax1.set_ylabel('Nº de Aulas')
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=tab_aulas)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Gráfico 2: Faturamento por Professor
        df_faturamento_prof = analyzers["financeiro"].get_faturamento_por_professor('2024')
        fig2 = Figure(figsize=(10, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(df_faturamento_prof['nome_professor'], df_faturamento_prof['faturamento_professor'], color='#d62728')
        ax2.set_title('Faturamento Gerado por Professor em 2024')
        ax2.set_ylabel('Valor (R$)')
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=tab_faturamento)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)