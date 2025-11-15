# ui/app.py

import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from tkcalendar import DateEntry # --- IMPORTAÇÃO DA NOVA BIBLIOTECA ---

# Importa as classes de cada tela
from .overview_view import OverviewView
from .finance_view import FinanceView
from .students_view import StudentsView
from .teachers_view import TeachersView
from .classes_view import ClassesView

# Importa a lógica de dados
from utils.data_handler import DataHandler
from analysis.alunos_analysis import AlunosAnalysis
from analysis.aulas_analysis import AulasAnalysis
from analysis.financeiro_analysis import FinanceiroAnalysis
from analysis.professores_analysis import ProfessoresAnalysis

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Academia Maestro - Dashboard")
        self.geometry("1400x850")
        ctk.set_appearance_mode("Light")
        
        self.APP_COLOR = "#1A3A7D"
        self.BG_COLOR = "#FFFFFF"

        self.data_handler = DataHandler()
        self.analyzers = {
            "alunos": AlunosAnalysis(self.data_handler),
            "aulas": AulasAnalysis(self.data_handler),
            "financeiro": FinanceiroAnalysis(self.data_handler),
            "professores": ProfessoresAnalysis(self.data_handler)
        }

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_sidebar()
        self.create_header()

        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.BG_COLOR)
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.current_frame_name = None # --- NOVA LINHA: para saber qual tela está ativa ---
        self.frames = {}
        self.setup_frames()
        self.show_frame("overview")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", background="#E1E1E1", foreground="black", font=("Calibri", 10, "bold"))
        style.map('Treeview', background=[('selected', self.APP_COLOR)])

        self.frames = {}
        self.setup_frames()
        self.show_frame("overview")

    def create_sidebar(self):
        sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#F5F5F5")
        sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sidebar_frame.grid_rowconfigure(7, weight=1)

        logo_image = ctk.CTkImage(Image.open("assets/logo.png"), size=(150, 150))
        logo_label = ctk.CTkLabel(sidebar_frame, image=logo_image, text="")
        logo_label.grid(row=0, column=0, padx=20, pady=20)

        buttons = {
            "Visão Geral": "overview", "Finanças": "finance", "Alunos": "students",
            "Professores": "teachers", "Aulas": "classes"
        }
        for i, (text, name) in enumerate(buttons.items(), 1):
            button = ctk.CTkButton(
                sidebar_frame, text=text, height=40,
                fg_color=self.APP_COLOR, hover_color="#112754",
                command=lambda n=name: self.show_frame(n)
            )
            button.grid(row=i, column=0, padx=20, pady=10, sticky="ew")

    def create_header(self):
        header_frame = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="transparent")
        header_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        ctk.CTkLabel(header_frame, text="Período:").pack(side="left", padx=(0, 10))
        
        # --- MUDANÇA: SUBSTITUINDO CTkEntry POR DateEntry ---
        self.start_date_entry = DateEntry(
            header_frame, 
            width=12, 
            background=self.APP_COLOR, 
            foreground='white', 
            borderwidth=2,
            font=('Calibri', 12),
            date_pattern='yyyy-mm-dd' # Formato de data consistente
        )
        self.start_date_entry.pack(side="left", padx=5)
        self.start_date_entry.set_date("2024-01-01") # Define data inicial

        ctk.CTkLabel(header_frame, text="até").pack(side="left", padx=5)

        self.end_date_entry = DateEntry(
            header_frame, 
            width=12, 
            background=self.APP_COLOR, 
            foreground='white', 
            borderwidth=2,
            font=('Calibri', 12),
            date_pattern='yyyy-mm-dd' # Formato de data consistente
        )
        self.end_date_entry.pack(side="left", padx=5)
        self.end_date_entry.set_date("2024-12-31") # Define data final

        self.apply_button = ctk.CTkButton(header_frame, text="Aplicar", fg_color=self.APP_COLOR, hover_color="#112754", command=self.apply_filters)
        self.apply_button.pack(side="left", padx=10)

    def apply_filters(self):
        # A forma de pegar a data continua a mesma
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        print(f"Filtro aplicado: de {start_date} a {end_date}")
        # Futuramente, aqui chamaremos a atualização dos gráficos
        
        if self.current_frame_name:
            current_frame = self.frames[self.current_frame_name]
            # Verifica se a tela tem um método de atualização antes de chamar
            if hasattr(current_frame, 'update_view'):
                current_frame.update_view(start_date, end_date)

    def setup_frames(self):
        views = {
            "overview": OverviewView, "finance": FinanceView, "students": StudentsView,
            "teachers": TeachersView, "classes": ClassesView
        }
        for name, ViewClass in views.items():
            frame = ViewClass(self.main_frame, self.analyzers, self.data_handler)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Mostra a tela solicitada e atualiza o seu estado."""
        self.current_frame_name = page_name # --- NOVA LINHA: atualiza a tela ativa ---
        frame = self.frames[page_name]
        # Atualiza a view com os filtros atuais sempre que trocamos de tela
        if hasattr(frame, 'update_view'):
             frame.update_view(self.start_date_entry.get(), self.end_date_entry.get())
        frame.tkraise()