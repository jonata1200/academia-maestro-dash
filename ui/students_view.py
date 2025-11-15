# ui/students_view.py

import customtkinter as ctk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import datetime
import matplotlib.patches as patches

class StudentsView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        
        self.analyzers = analyzers
        self.data_handler = data_handler

        title_label = ctk.CTkLabel(self, text="Dashboard de Alunos", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        # --- LAYOUT DOS KPIs ATUALIZADO PARA 2x2 ---
        self.kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_container.pack(fill="x", padx=10, pady=10)
        self.kpi_container.grid_columnconfigure((0, 1), weight=1) # 2 colunas
        self.kpi_container.grid_rowconfigure((0, 1), weight=1)    # 2 linhas

        # Abas
        self.tab_view = ctk.CTkTabview(self, height=500, fg_color="#F5F5F5")
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        self.tab_lista = self.tab_view.add("Lista de Alunos")
        self.tab_matriculas = self.tab_view.add("Evolução de Matrículas")
        self.tab_demografia = self.tab_view.add("Público-Alvo")

    def update_view(self, start_date, end_date):
        for widget in self.kpi_container.winfo_children(): widget.destroy()
        
        # --- LÓGICA DE ATUALIZAÇÃO DOS KPIS ---
        # KPIs Gerais
        total_alunos = len(self.data_handler.get_data('alunos'))
        total_ativos = self.analyzers["alunos"].get_total_alunos('Ativo')
        
        # KPI de Novas Matrículas (depende do período)
        df_matriculas = self.analyzers["alunos"].get_novas_matriculas_por_mes(start_date, end_date)
        novas_matriculas = df_matriculas['novas_matriculas'].sum()

        # KPI de Evasão (Churn)
        churn_data = self.analyzers["alunos"].get_churn_kpis()
        taxa_evasao = churn_data["taxa_evasao"]

        # --- EXIBIÇÃO DOS KPIS EM GRID 2x2 ---
        kpi_font = ctk.CTkFont(size=20)
        ctk.CTkLabel(self.kpi_container, text=f"Total de Alunos\n{total_alunos}", font=kpi_font).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self.kpi_container, text=f"Alunos Ativos\n{total_ativos}", font=kpi_font).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self.kpi_container, text=f"Novas Matrículas (Período)\n{novas_matriculas}", font=kpi_font).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        # KPI de Evasão com formatação condicional de cor
        churn_color = "red" if taxa_evasao > 20 else "green" # Fica vermelho se a evasão for > 20%
        ctk.CTkLabel(self.kpi_container, text=f"Taxa de Evasão (Geral)\n{taxa_evasao:.1f}%", font=kpi_font, text_color=churn_color).grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Atualiza o conteúdo das abas
        self.update_tabs_content(df_matriculas)


    def update_tabs_content(self, df_matriculas):
        # Limpa o conteúdo anterior das abas
        for tab in [self.tab_lista, self.tab_matriculas, self.tab_demografia]:
            for widget in tab.winfo_children():
                widget.destroy()

        # Redesenha o conteúdo de cada aba
        self.create_students_list(self.tab_lista, self.data_handler)
        self.create_enrollment_chart(self.tab_matriculas, df_matriculas)
        self.create_demographics_charts(self.tab_demografia, self.data_handler)

    # (O restante dos métodos create_* permanecem os mesmos)
    def create_students_list(self, tab, data_handler):
        alunos_df = data_handler.get_data('alunos')
        cols = ['id', 'nome', 'email', 'telefone', 'data_cadastro', 'status']
        tree = ttk.Treeview(tab, columns=cols, show='headings')
        for col in cols: tree.heading(col, text=col.capitalize())
        for _, row in alunos_df.iterrows(): tree.insert("", "end", values=list(row[cols]))
        tree.pack(fill="both", expand=True)

    def create_enrollment_chart(self, tab, df_matriculas):
        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)

        if not df_matriculas.empty:
            ax.plot(df_matriculas['mes'], df_matriculas['novas_matriculas'], marker='o', color='#1A3A7D')
            ax.set_title('Novas Matrículas por Mês', color='black')
            ax.set_ylabel('Nº de Matrículas', color='black')
            ax.tick_params(axis='x', colors='black', rotation=45)
            ax.tick_params(axis='y', colors='black')
        else:
            ax.text(0.5, 0.5, 'Nenhuma matrícula no período selecionado', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12, color='gray')
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_demographics_charts(self, tab, data_handler):
        alunos_df = data_handler.get_data('alunos')
        today = datetime.date.today()
        alunos_df['data_nascimento'] = pd.to_datetime(alunos_df['data_nascimento'], errors='coerce')
        alunos_df['idade'] = alunos_df['data_nascimento'].apply(lambda dob: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)) if pd.notna(dob) else None)
        bins = [0, 17, 25, 35, 50, 100]
        labels = ['Menor de 18', '18-25 anos', '26-35 anos', '36-50 anos', '51+ anos']
        alunos_df['faixa_etaria'] = pd.cut(alunos_df['idade'], bins=bins, labels=labels, right=False)
        charts_container = ctk.CTkFrame(tab, fg_color="transparent")
        charts_container.pack(fill="both", expand=True)
        charts_container.grid_columnconfigure((0, 1), weight=1)
        alunos_genero_filtrado = alunos_df[alunos_df['genero'].isin(['Feminino', 'Masculino'])]
        gender_counts = alunos_genero_filtrado['genero'].value_counts()
        fig_gender = Figure(figsize=(3.5, 3.5), dpi=100)
        ax_gender = fig_gender.add_subplot(111)
        wedges, texts, autotexts = ax_gender.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, pctdistance=0.85, colors=['#1A3A7D', '#2E7D32'])
        centre_circle = patches.Circle((0, 0), 0.70, fc='white')
        ax_gender.add_artist(centre_circle)
        ax_gender.axis('equal')
        ax_gender.set_title('Distribuição por Gênero', color='black')
        for text in texts: text.set_color('black')
        for autotext in autotexts: autotext.set_color('white')
        fig_gender.tight_layout()
        canvas_gender = FigureCanvasTkAgg(fig_gender, master=charts_container)
        canvas_gender.draw()
        canvas_gender.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        age_counts = alunos_df['faixa_etaria'].value_counts().sort_index()
        fig_age = Figure(figsize=(3.5, 3.5), dpi=100)
        ax_age = fig_age.add_subplot(111)
        wedges, texts, autotexts = ax_age.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
        centre_circle = patches.Circle((0, 0), 0.70, fc='white')
        ax_age.add_artist(centre_circle)
        ax_age.axis('equal')
        ax_age.set_title('Distribuição por Faixa Etária', color='black')
        for text in texts: text.set_color('black')
        for autotext in autotexts: autotext.set_color('white')
        fig_age.tight_layout()
        canvas_age = FigureCanvasTkAgg(fig_age, master=charts_container)
        canvas_age.draw()
        canvas_age.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")