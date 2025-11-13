# ui/students_view.py

import customtkinter as ctk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StudentsView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        
        title_label = ctk.CTkLabel(self, text="Dashboard de Alunos", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        kpi_container.pack(fill="x", padx=10, pady=10)
        kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        total_alunos = len(data_handler.get_data('alunos'))
        total_ativos = analyzers["alunos"].get_total_alunos('Ativo')
        df_matriculas = analyzers["alunos"].get_novas_matriculas_por_mes('2024')
        novas_matriculas = df_matriculas['novas_matriculas'].sum()

        ctk.CTkLabel(kpi_container, text=f"Total de Alunos\n{total_alunos}", font=ctk.CTkFont(size=20)).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(kpi_container, text=f"Alunos Ativos\n{total_ativos}", font=ctk.CTkFont(size=20)).grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkLabel(kpi_container, text=f"Novas Matrículas (2024)\n{novas_matriculas}", font=ctk.CTkFont(size=20)).grid(row=0, column=2, padx=10, sticky="ew")

        tab_view = ctk.CTkTabview(self, height=500)
        tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        tab_lista = tab_view.add("Lista de Alunos")
        tab_matriculas = tab_view.add("Evolução de Matrículas")

        # Tabela 1: Lista de Alunos
        alunos_df = data_handler.get_data('alunos')
        cols = ['id', 'nome', 'email', 'telefone', 'data_cadastro', 'status']
        tree = ttk.Treeview(tab_lista, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col.capitalize())
        for _, row in alunos_df.iterrows():
            tree.insert("", "end", values=list(row[cols]))
        tree.pack(fill="both", expand=True)

        # Gráfico 2: Evolução de Matrículas
        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(df_matriculas['mes'], df_matriculas['novas_matriculas'], marker='o', color='#1A3A7D')
        ax.set_title('Novas Matrículas por Mês em 2024')
        ax.set_ylabel('Nº de Matrículas')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=tab_matriculas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)