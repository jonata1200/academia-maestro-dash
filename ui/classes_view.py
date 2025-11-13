# ui/classes_view.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches # Importa a biblioteca para desenhar formas

class ClassesView(ctk.CTkFrame):
    def __init__(self, master, analyzers, data_handler):
        super().__init__(master, fg_color="transparent")
        
        title_label = ctk.CTkLabel(self, text="Dashboard de Aulas", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20), padx=10)

        kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        kpi_container.pack(fill="x", padx=10, pady=10)
        kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        df_status = analyzers["aulas"].get_total_aulas_por_status('2024')
        total_aulas = df_status['total_aulas'].sum()
        concluidas = df_status.query("status == 'Concluída'")['total_aulas'].iloc[0] if not df_status.query("status == 'Concluída'").empty else 0
        taxa_conclusao = (concluidas / total_aulas) * 100 if total_aulas > 0 else 0

        ctk.CTkLabel(kpi_container, text=f"Total de Aulas (2024)\n{total_aulas}", font=ctk.CTkFont(size=20)).grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(kpi_container, text=f"Aulas Concluídas\n{concluidas}", font=ctk.CTkFont(size=20)).grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkLabel(kpi_container, text=f"Taxa de Conclusão\n{taxa_conclusao:.1f}%", font=ctk.CTkFont(size=20)).grid(row=0, column=2, padx=10, sticky="ew")

        tab_view = ctk.CTkTabview(self, height=500, fg_color="#F5F5F5")
        tab_view.pack(fill="both", expand=True, padx=10, pady=20)
        
        tab_status = tab_view.add("Distribuição por Status")
        tab_popularidade = tab_view.add("Aulas por Instrumento")

        # --- INÍCIO DA MODIFICAÇÃO PARA GRÁFICO DE ROSCA ---
        
        # Gráfico 1: Status (agora Donut Chart)
        fig1 = Figure(figsize=(10, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        
        if not df_status.empty:
            # Define cores personalizadas
            colors = ["#EC7412", "#D32811", "#14D11E"] # Verde para Concluída, Laranja para Cancelada, Azul para Agendada
            
            # Cria o gráfico de pizza (a base do donut)
            wedges, texts, autotexts = ax1.pie(
                df_status['total_aulas'], 
                labels=df_status['status'], 
                autopct='%1.1f%%', 
                startangle=90,
                colors=colors,
                pctdistance=0.85 # Move os números de porcentagem para dentro do anel
            )
            
            # Desenha um círculo branco no centro para criar o efeito "donut"
            centre_circle = patches.Circle((0, 0), 0.70, fc='white')
            ax1.add_artist(centre_circle)

            # Garante que o gráfico seja um círculo perfeito
            ax1.axis('equal')  

            # Ajusta o título e as cores do texto para o tema claro
            ax1.set_title('Distribuição de Status das Aulas em 2024', color='black')
            for text in texts:
                text.set_color('black')
            for autotext in autotexts:
                autotext.set_color('white') # Texto da porcentagem em branco para melhor contraste

        canvas1 = FigureCanvasTkAgg(fig1, master=tab_status)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)
        
        # --- FIM DA MODIFICAÇÃO ---

        # Gráfico 2: Popularidade
        df_popularidade = analyzers["aulas"].get_popularidade_instrumentos()
        fig2 = Figure(figsize=(10, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(df_popularidade['nome_instrumento'], df_popularidade['total_aulas_agendadas'], color='#1A3A7D')
        ax2.set_title('Popularidade dos Instrumentos (Todas as Aulas)', color='black')
        ax2.set_ylabel('Nº de Aulas Agendadas', color='black')
        ax2.tick_params(axis='x', colors='black')
        ax2.tick_params(axis='y', colors='black')
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=tab_popularidade)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)