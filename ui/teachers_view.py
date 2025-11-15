# ui/teachers_view.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class TeachersView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        
        self.analyzers = analyzers
        self.data_handler = data_handler

        title_label = ctk.CTkLabel(self, text="Dashboard de Professores", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)
        
        # Container para os KPIs
        self.kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_container.pack(fill="x", padx=10, pady=10)
        self.kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Abas
        self.tab_view = ctk.CTkTabview(self, height=500, fg_color="#F5F5F5")
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        self.tab_carga_aulas = self.tab_view.add("Carga Horária (Aulas)")
        self.tab_carga_horas = self.tab_view.add("Carga Horária (Horas)")
        self.tab_instrumentos = self.tab_view.add("Instrumentos Lecionados")

    def update_view(self, start_date, end_date):
        """Atualiza a tela com base no período selecionado."""
        for widget in self.kpi_container.winfo_children(): widget.destroy()

        # Busca os dados de carga horária para o período
        df_carga_horaria = self.analyzers["professores"].get_carga_horaria_professor(start_date, end_date)

        # Calcula e exibe os KPIs
        total_prof_ativos = len(self.data_handler.get_data('professores').query("status == 'Ativo'"))
        total_horas = df_carga_horaria['horas_lecionadas'].sum()
        media_horas_prof = df_carga_horaria['horas_lecionadas'].mean() if not df_carga_horaria.empty else 0

        kpi_font = ctk.CTkFont(size=20)
        ctk.CTkLabel(self.kpi_container, text=f"Professores Ativos\n{total_prof_ativos}", font=kpi_font).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(self.kpi_container, text=f"Total de Horas Lecionadas\n{total_horas:.1f}", font=kpi_font).grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkLabel(self.kpi_container, text=f"Média de Horas por Professor\n{media_horas_prof:.1f}", font=kpi_font).grid(row=0, column=2, padx=10, sticky="ew")

        # Atualiza o conteúdo das abas
        self.update_tabs_content(df_carga_horaria)

    def update_tabs_content(self, df_carga_horaria):
        # Limpa o conteúdo anterior das abas
        for tab in [self.tab_carga_aulas, self.tab_carga_horas, self.tab_instrumentos]:
            for widget in tab.winfo_children():
                widget.destroy()

        # Gráfico 1: Aulas por Professor
        fig1 = Figure(figsize=(10, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        if not df_carga_horaria.empty:
            ax1.bar(df_carga_horaria['nome_professor'], df_carga_horaria['aulas_concluidas'], color='#ff7f0e')
            ax1.set_title('Aulas Concluídas por Professor no Período', color='black')
            ax1.set_ylabel('Nº de Aulas', color='black')
            ax1.tick_params(axis='x', colors='black', rotation=45)
            ax1.tick_params(axis='y', colors='black')
        else:
            ax1.text(0.5, 0.5, 'Nenhum dado de aula no período', ha='center', va='center', transform=ax1.transAxes)
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=self.tab_carga_aulas)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Gráfico 2: Horas por Professor
        fig2 = Figure(figsize=(10, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        if not df_carga_horaria.empty:
            df_sorted_by_hours = df_carga_horaria.sort_values('horas_lecionadas', ascending=False)
            ax2.bar(df_sorted_by_hours['nome_professor'], df_sorted_by_hours['horas_lecionadas'], color='#d62728')
            ax2.set_title('Horas Lecionadas por Professor no Período', color='black')
            ax2.set_ylabel('Total de Horas', color='black')
            ax2.tick_params(axis='x', colors='black', rotation=45)
            ax2.tick_params(axis='y', colors='black')
        else:
            ax2.text(0.5, 0.5, 'Nenhum dado de hora no período', ha='center', va='center', transform=ax2.transAxes)
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=self.tab_carga_horas)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)
        
        # (A aba de instrumentos não precisa ser interativa com o filtro de data, por enquanto)