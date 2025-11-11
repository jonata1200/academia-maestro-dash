# main.py

import pandas as pd
import datetime
from utils.data_handler import DataHandler
from analysis.alunos_analysis import AlunosAnalysis
from analysis.aulas_analysis import AulasAnalysis
from analysis.financeiro_analysis import FinanceiroAnalysis
from analysis.professores_analysis import ProfessoresAnalysis

class AcademiaMaestroApp:
    def __init__(self):
        """Inicializa a aplicação, o DataHandler e todas as classes de análise."""
        self.data_handler = DataHandler()
        # Injeta a instância do data_handler nos analisadores
        self.alunos_analyser = AlunosAnalysis(self.data_handler)
        self.aulas_analyser = AulasAnalysis(self.data_handler)
        self.financeiro_analyser = FinanceiroAnalysis(self.data_handler)
        self.professores_analyser = ProfessoresAnalysis(self.data_handler)
        print("Academia Maestro App (Modo Excel) inicializado.")

    def _get_next_id(self, table_name):
        """Calcula o próximo ID para uma nova entrada em uma tabela (aba)."""
        df = self.data_handler.get_data(table_name)
        if df.empty or 'id' not in df.columns:
            return 1
        return df['id'].max() + 1

    def setup_data_source(self):
        """Garante que o arquivo Excel e suas abas existam."""
        print("\n--- Verificando a fonte de dados Excel ---")
        self.data_handler.initialize_excel_file()
        print("Fonte de dados pronta.")
        
    def seed_initial_data(self):
        """Popula o Excel com dados iniciais se estiver vazio."""
        print("\n--- Verificando dados iniciais (seed) ---")
        
        # Adiciona instrumentos se não existirem
        if self.data_handler.get_data('instrumentos').empty:
            print("Populando instrumentos...")
            instrumentos_df = pd.DataFrame([
                {'id': 1, 'nome_instrumento': 'Violão'},
                {'id': 2, 'nome_instrumento': 'Teclado'},
                {'id': 3, 'nome_instrumento': 'Guitarra'},
            ])
            self.data_handler.insert_data('instrumentos', instrumentos_df)

        # Adiciona professores se não existirem
        if self.data_handler.get_data('professores').empty:
            print("Populando professores...")
            professores_df = pd.DataFrame([
                {'id': 1, 'nome': 'Ana Silva', 'email': 'ana.silva@maestro.com', 'especializacao': 'Violão'},
                {'id': 2, 'nome': 'Carlos Mendes', 'email': 'carlos.mendes@maestro.com', 'especializacao': 'Teclado'},
            ])
            self.data_handler.insert_data('professores', professores_df)
            
    def add_new_aluno(self, nome, data_nascimento, genero, email, telefone):
        """Adiciona um novo aluno ao sistema."""
        print(f"\n--- Adicionando novo aluno: {nome} ---")
        new_aluno_data = {
            'id': self._get_next_id('alunos'),
            'nome': nome,
            'data_nascimento': data_nascimento,
            'genero': genero,
            'email': email,
            'telefone': telefone,
            'data_cadastro': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Ativo'
        }
        self.data_handler.insert_data('alunos', pd.DataFrame([new_aluno_data]))
        print(f"Aluno {nome} adicionado com sucesso.")

    def schedule_aula(self, aluno_id, professor_id, instrumento_id, data_aula_str, hora_inicio_str, hora_fim_str, valor_aula=250.00):
        """Agenda uma nova aula individual."""
        print(f"\n--- Agendando aula para Aluno ID: {aluno_id} ---")
        new_aula_data = {
            'id': self._get_next_id('agenda_aulas'),
            'aluno_id': aluno_id,
            'professor_id': professor_id,
            'instrumento_id': instrumento_id,
            'data_aula': data_aula_str,
            'hora_inicio': hora_inicio_str,
            'hora_fim': hora_fim_str,
            'valor_aula': valor_aula,
            'status': 'Agendada',
            'observacoes': ''
        }
        self.data_handler.insert_data('agenda_aulas', pd.DataFrame([new_aula_data]))
        print(f"Aula agendada para {data_aula_str} às {hora_inicio_str}.")

    def register_payment(self, aluno_id, valor_pago, metodo_pagamento, referencia_aula_id=None):
        """Registra um pagamento de um aluno."""
        print(f"\n--- Registrando pagamento para Aluno ID: {aluno_id} ---")
        new_payment_data = {
            'id': self._get_next_id('pagamentos'),
            'aluno_id': aluno_id,
            'data_pagamento': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'valor_pago': valor_pago,
            'metodo_pagamento': metodo_pagamento,
            'referencia_aula_id': referencia_aula_id,
            'status': 'Pago',
            'observacoes': ''
        }
        self.data_handler.insert_data('pagamentos', pd.DataFrame([new_payment_data]))
        print(f"Pagamento de R${valor_pago:.2f} registrado.")

    def run_all_analysis(self, year='2024'):
        """Executa e imprime todas as análises disponíveis."""
        print(f"\n======== EXECUTANDO ANÁLISES PARA O ANO {year} ========")

        # --- Análise de Alunos ---
        print("\n--- Análise de Alunos ---")
        total_ativos = self.alunos_analyser.get_total_alunos(status='Ativo')
        print(f"Total de alunos ativos: {total_ativos}")
        
        # --- Análise de Aulas ---
        print("\n--- Análise de Aulas ---")
        total_aulas_status = self.aulas_analyser.get_total_aulas_por_status(year)
        print(f"\nTotal de aulas por status ({year}):")
        print(total_aulas_status.to_string(index=False))

        popularidade_instr = self.aulas_analyser.get_popularidade_instrumentos()
        print("\nPopularidade dos instrumentos:")
        print(popularidade_instr.to_string(index=False))
        
        aulas_prof = self.aulas_analyser.get_aulas_por_professor(year)
        print(f"\nAulas concluídas por professor ({year}):")
        print(aulas_prof.to_string(index=False))

        # --- Análise Financeira ---
        print("\n--- Análise Financeira ---")
        faturamento_mensal = self.financeiro_analyser.get_faturamento_total_por_mes(year)
        print(f"\nFaturamento total por mês ({year}):")
        print(faturamento_mensal.to_string(index=False))
        
        faturamento_instrumento = self.financeiro_analyser.get_faturamento_por_instrumento(year)
        print(f"\nFaturamento por instrumento ({year}):")
        print(faturamento_instrumento.to_string(index=False))

        # --- Análise de Professores ---
        print("\n--- Análise de Professores ---")
        carga_horaria = self.professores_analyser.get_carga_horaria_professor(year)
        print(f"\nCarga horária por professor ({year}):")
        print(carga_horaria.to_string(index=False))

        instrumentos_prof = self.professores_analyser.get_instrumentos_por_professor()
        print("\nInstrumentos lecionados por professor:")
        print(instrumentos_prof.to_string(index=False))

        print("\n======== ANÁLISES CONCLUÍDAS ========")

# Função principal para executar o aplicativo
if __name__ == "__main__":
    app = AcademiaMaestroApp()

    # 1. Configura a fonte de dados (cria o .xlsx se não existir) e popula dados básicos
    app.setup_data_source()
    app.seed_initial_data()

    # 2. Exemplo de operações
    print("\n--- EXEMPLOS DE OPERAÇÕES ---")
    app.add_new_aluno("Gabriela Pereira", "1995-03-10", "Feminino", "gabriela.p@email.com", "11912345678")
    
    # Buscar IDs de exemplo para usar nas operações
    alunos_df = app.data_handler.get_data('alunos')
    professores_df = app.data_handler.get_data('professores')
    instrumentos_df = app.data_handler.get_data('instrumentos')
    
    # Busca o ID da aluna que acabamos de adicionar (com tratamento de erro)
    gabi_info = alunos_df[alunos_df['email'] == 'gabriela.p@email.com']
    aluno_gabi_id = gabi_info['id'].iloc[0] if not gabi_info.empty else None

    # Busca IDs de dados do seed (com tratamento de erro)
    ana_info = professores_df[professores_df['nome'] == 'Ana Silva']
    prof_ana_id = ana_info['id'].iloc[0] if not ana_info.empty else 1

    violao_info = instrumentos_df[instrumentos_df['nome_instrumento'] == 'Violão']
    violao_id = violao_info['id'].iloc[0] if not violao_info.empty else 1
    
    # Agendar e pagar aulas apenas se o aluno foi encontrado
    if aluno_gabi_id:
        app.schedule_aula(aluno_gabi_id, prof_ana_id, violao_id, '2024-07-25', '10:00', '11:00')

        # Para registrar o pagamento, buscamos o ID da aula recém-agendada
        agenda_df = app.data_handler.get_data('agenda_aulas')
        aulas_gabi = agenda_df[agenda_df['aluno_id'] == aluno_gabi_id].sort_values('id', ascending=False)
        
        if not aulas_gabi.empty:
            ultima_aula_id = aulas_gabi['id'].iloc[0]
            app.register_payment(aluno_gabi_id, 250.00, 'Pix', ultima_aula_id)

    # 3. Executar todas as análises
    app.run_all_analysis(year='2024')

    print("\nAplicação Academia Maestro encerrada.")