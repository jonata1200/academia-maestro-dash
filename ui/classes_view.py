# ui/classes_view.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import pandas as pd

class ClassesView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        
        self.analyzers = analyzers
        self.data_handler = data_handler

        title_label = ctk.CTkLabel(self, text="Dashboard de Aulas", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        self.kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_container.pack(fill="x", padx=10, pady=10)
        self.kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        self.tab_view = ctk.CTkTabview(self, height=500, fg_color="#F5F5F5")
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        self.tab_status = self.tab_view.add("Distribuição por Status")
        self.tab_popularidade = self.tab_view.add("Aulas por Instrumento")
        self.tab_pico = self.tab_view.add("Horários de Pico")

    def update_view(self, start_date, end_date):
        """Atualiza todos os componentes da tela com base no período."""
        for widget in self.kpi_container.winfo_children():
            widget.destroy()

        # --- CORREÇÃO APLICADA AQUI ---
        # Agora passamos o start_date e end_date para a função de análise
        df_status = self.analyzers["aulas"].get_total_aulas_por_status(start_date, end_date)
        heatmap_data = self.analyzers["aulas"].get_peak_hours_data(start_date, end_date)
        
        total_aulas = df_status['total_aulas'].sum()
        concluidas_series = df_status.query("status == 'Concluída'")['total_aulas']
        concluidas = concluidas_series.iloc[0] if not concluidas_series.empty else 0
        taxa_conclusao = (concluidas / total_aulas) * 100 if total_aulas > 0 else 0

        kpi_font = ctk.CTkFont(size=20)
        ctk.CTkLabel(self.kpi_container, text=f"Total de Aulas no Período\n{total_aulas}", font=kpi_font).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(self.kpi_container, text=f"Aulas Concluídas\n{concluidas}", font=kpi_font).grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkLabel(self.kpi_container, text=f"Taxa de Conclusão\n{taxa_conclusao:.1f}%", font=kpi_font).grid(row=0, column=2, padx=10, sticky="ew")
        
        self.update_tabs_content(start_date, end_date, df_status, heatmap_data)

    def update_tabs_content(self, start_date, end_date, df_status, heatmap_data):
        for tab in [self.tab_status, self.tab_popularidade, self.tab_pico]:
            for widget in tab.winfo_children():
                widget.destroy()
        
        self.create_status_chart(self.tab_status, df_status)
        # Passando as datas para a popularidade também
        df_popularidade = self.analyzers["aulas"].get_popularidade_instrumentos(start_date, end_date)
        self.create_popularity_chart(self.tab_popularidade, df_popularidade)
        self.create_heatmap_chart(self.tab_pico, heatmap_data)

    def create_status_chart(self, tab, df_status):
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        if not df_status.empty:
            colors = ['#2E7D32', '#F47A20', '#1A3A7D']
            wedges, texts, autotexts = ax.pie(
                df_status['total_aulas'], labels=df_status['status'], autopct='%1.1f%%',
                startangle=90, pctdistance=0.85, colors=colors
            )
            centre_circle = patches.Circle((0, 0), 0.70, fc='white')
            ax.add_artist(centre_circle)
            ax.axis('equal')
            ax.set_title('Distribuição de Status no Período', color='black')
            for text in texts: text.set_color('black')
            for autotext in autotexts: autotext.set_color('white')
        
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_popularity_chart(self, tab, df_popularidade):
        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(df_popularidade['nome_instrumento'], df_popularidade['total_aulas_agendadas'], color='#1A3A7D')
        ax.set_title('Popularidade dos Instrumentos no Período', color='black')
        ax.set_ylabel('Nº de Aulas Agendadas', color='black')
        ax.tick_params(axis='x', colors='black', rotation=45)
        ax.tick_params(axis='y', colors='black')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_heatmap_chart(self, tab, data):
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)

        if not data.empty:
            im = ax.imshow(data, cmap="viridis", aspect="auto")
            fig.colorbar(im, ax=ax, label="Nº de Aulas")
            ax.set_xticks(range(len(data.columns)))
            ax.set_xticklabels(data.columns.astype(int))
            ax.set_yticks(range(len(data.index)))
            ax.set_yticklabels(data.index)
            ax.set_xlabel("Hora do Dia")
            ax.set_ylabel("Dia da Semana")
            ax.set_title("Concentração de Aulas por Dia e Hora")
        else:
            ax.text(0.5, 0.5, 'Nenhuma aula no período selecionado', ha='center', va='center', transform=ax.transAxes, color='gray')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)