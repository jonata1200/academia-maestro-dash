# ui/finance_view.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class FinanceView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        
        # Título da Tela
        title_label = ctk.CTkLabel(self, text="Dashboard Financeiro", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        # Container para os KPIs
        kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        kpi_container.pack(fill="x", padx=10, pady=10)
        kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Calculando os KPIs
        df_pagamentos_2024 = analyzers["financeiro"].get_faturamento_total_por_mes('2024')
        receita_total = df_pagamentos_2024['faturamento_mensal'].sum()
        aulas_pagas = len(data_handler.get_data('pagamentos').query("status == 'Pago' and data_pagamento.str.startswith('2024')"))
        ticket_medio = (receita_total / aulas_pagas) if aulas_pagas > 0 else 0

        # Criando os Cards de KPI
        ctk.CTkLabel(kpi_container, text=f"Receita Total (2024)\nR$ {receita_total:,.2f}", font=ctk.CTkFont(size=20)).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(kpi_container, text=f"Aulas Pagas (2024)\n{aulas_pagas}", font=ctk.CTkFont(size=20)).grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkLabel(kpi_container, text=f"Ticket Médio\nR$ {ticket_medio:,.2f}", font=ctk.CTkFont(size=20)).grid(row=0, column=2, padx=10, sticky="ew")

        # Abas de Visualização
        tab_view = ctk.CTkTabview(self, height=500)
        tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        tab_evolucao = tab_view.add("Evolução Mensal")
        tab_por_instrumento = tab_view.add("Faturamento por Instrumento")
        tab_extrato = tab_view.add("Extrato Detalhado")

        # Gráfico 1: Evolução Mensal
        fig1 = Figure(figsize=(10, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.bar(df_pagamentos_2024['mes'], df_pagamentos_2024['faturamento_mensal'], color='#4a0072')
        ax1.set_title('Evolução do Faturamento em 2024')
        ax1.set_ylabel('Valor (R$)')
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=tab_evolucao)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Gráfico 2: Faturamento por Instrumento
        df_instr = analyzers["financeiro"].get_faturamento_por_instrumento('2024')
        fig2 = Figure(figsize=(10, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(df_instr['nome_instrumento'], df_instr['faturamento_instrumento'], color='#00a152')
        ax2.set_title('Faturamento por Instrumento em 2024')
        ax2.set_ylabel('Valor (R$)')
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=tab_por_instrumento)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)
        
        # Tabela 3: Extrato
        df_pagamentos_full = data_handler.get_data('pagamentos')
        cols = ['id', 'aluno_id', 'data_pagamento', 'valor_pago', 'metodo_pagamento', 'status']
        tree = ttk.Treeview(tab_extrato, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col.capitalize())
        for _, row in df_pagamentos_full.iterrows():
            tree.insert("", "end", values=list(row[cols]))
        tree.pack(fill="both", expand=True)