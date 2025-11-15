# ui/finance_view.py
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class FinanceView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        self.analyzers = analyzers
        self.data_handler = data_handler
        
        title_label = ctk.CTkLabel(self, text="Dashboard Financeiro", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        self.kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_container.pack(fill="x", padx=10, pady=10)
        self.kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        self.tab_view = ctk.CTkTabview(self, height=500, fg_color="#F5F5F5")
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        self.tab_evolucao = self.tab_view.add("Evolução Mensal")
        self.tab_por_instrumento = self.tab_view.add("Faturamento por Instrumento")
        self.tab_extrato = self.tab_view.add("Extrato Detalhado")

    def update_view(self, start_date, end_date):
        for widget in self.kpi_container.winfo_children(): widget.destroy()

        df_faturamento = self.analyzers["financeiro"].get_faturamento_total_por_mes(start_date, end_date)
        receita_total = df_faturamento['faturamento_mensal'].sum()
        
        pagamentos_periodo = self.analyzers["financeiro"]._filter_pagamentos_by_date(start_date, end_date)
        aulas_pagas = len(pagamentos_periodo)
        ticket_medio = (receita_total / aulas_pagas) if aulas_pagas > 0 else 0

        ctk.CTkLabel(self.kpi_container, text=f"Receita no Período\nR$ {receita_total:,.2f}", font=ctk.CTkFont(size=20)).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(self.kpi_container, text=f"Aulas Pagas no Período\n{aulas_pagas}", font=ctk.CTkFont(size=20)).grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkLabel(self.kpi_container, text=f"Ticket Médio\nR$ {ticket_medio:,.2f}", font=ctk.CTkFont(size=20)).grid(row=0, column=2, padx=10, sticky="ew")

        self.update_tabs_content(start_date, end_date, df_faturamento, pagamentos_periodo)

    def update_tabs_content(self, start_date, end_date, df_faturamento, pagamentos_periodo):
        for tab in [self.tab_evolucao, self.tab_por_instrumento, self.tab_extrato]:
            for widget in tab.winfo_children(): widget.destroy()
        
        # Gráfico 1: Evolução Mensal
        fig1 = Figure(figsize=(10, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.bar(df_faturamento['mes'], df_faturamento['faturamento_mensal'], color='#4a0072')
        ax1.set_title('Evolução do Faturamento no Período', color='black')
        ax1.set_ylabel('Valor (R$)', color='black')
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=self.tab_evolucao)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Gráfico 2: Faturamento por Instrumento
        df_instr = self.analyzers["financeiro"].get_faturamento_por_instrumento(start_date, end_date)
        fig2 = Figure(figsize=(10, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(df_instr['nome_instrumento'], df_instr['faturamento_instrumento'], color='#00a152')
        ax2.set_title('Faturamento por Instrumento no Período', color='black')
        ax2.set_ylabel('Valor (R$)', color='black')
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=self.tab_por_instrumento)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)
        
        # Tabela 3: Extrato
        cols = ['id', 'aluno_id', 'data_pagamento', 'valor_pago', 'metodo_pagamento', 'status']
        tree = ttk.Treeview(self.tab_extrato, columns=cols, show='headings')
        for col in cols: tree.heading(col, text=col.capitalize())
        pagamentos_periodo['data_pagamento'] = pagamentos_periodo['data_pagamento'].dt.strftime('%Y-%m-%d')
        for _, row in pagamentos_periodo.iterrows(): tree.insert("", "end", values=list(row[cols]))
        tree.pack(fill="both", expand=True)