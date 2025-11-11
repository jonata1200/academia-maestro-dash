from utils.data_handler import DataHandler
from analysis.alunos_analysis import AlunosAnalysis
from analysis.aulas_analysis import AulasAnalysis
from analysis.financeiro_analysis import FinanceiroAnalysis
from analysis.professores_analysis import ProfessoresAnalysis
from etl.migrate_csv_to_sqlite import DatabaseMigrator
import datetime
import os

class AcademiaMaestroApp:
    def __init__(self):
        self.data_handler = DataHandler()
        self.alunos_analyser = AlunosAnalysis()
        self.aulas_analyser = AulasAnalysis()
        self.financeiro_analyser = FinanceiroAnalysis()
        self.professores_analyser = ProfessoresAnalysis()
        print("Academia Maestro App inicializado.")

    def setup_database(self, years=['2024']):
        """
        Configura o banco de dados (cria tabelas e popula dados iniciais/migra CSVs).
        """
        print("\n--- Configurando o Banco de Dados ---")
        migrator = DatabaseMigrator()
        migrator.run_full_migration(years=years)
        print("Configuração do banco de dados concluída.")

    def add_new_aluno(self, nome, data_nascimento, genero, email, telefone):
        """
        Adiciona um novo aluno ao sistema.
        """
        print(f"\n--- Adicionando novo aluno: {nome} ---")
        new_aluno_df = pd.DataFrame([{
            'nome': nome,
            'data_nascimento': data_nascimento,
            'genero': genero,
            'email': email,
            'telefone': telefone,
            'data_cadastro': datetime.datetime.now(),
            'status': 'Ativo'
        }])
        self.data_handler.insert_data_into_db('alunos', new_aluno_df)
        print(f"Aluno {nome} adicionado com sucesso.")

    def schedule_aula(self, aluno_id, professor_id, instrumento_id, data_aula_str, hora_inicio_str, hora_fim_str, valor_aula=250.00, observacoes=""):
        """
        Agenda uma nova aula individual.
        """
        print(f"\n--- Agendando aula para Aluno ID: {aluno_id} ---")
        # Garante que as datas e horas estão no formato correto para o DB
        data_aula = datetime.datetime.strptime(data_aula_str, '%Y-%m-%d').date()
        hora_inicio = datetime.datetime.strptime(hora_inicio_str, '%H:%M').time()
        hora_fim = datetime.datetime.strptime(hora_fim_str, '%H:%M').time()

        new_aula_df = pd.DataFrame([{
            'aluno_id': aluno_id,
            'professor_id': professor_id,
            'instrumento_id': instrumento_id,
            'data_aula': data_aula,
            'hora_inicio': hora_inicio,
            'hora_fim': hora_fim,
            'valor_aula': valor_aula,
            'status': 'Agendada',
            'observacoes': observacoes
        }])
        self.data_handler.insert_data_into_db('agenda_aulas', new_aula_df)
        print(f"Aula agendada para {data_aula_str} às {hora_inicio_str}.")

    def register_payment(self, aluno_id, valor_pago, metodo_pagamento, referencia_aula_id=None, observacoes=""):
        """
        Registra um pagamento de um aluno, opcionalmente associado a uma aula.
        """
        print(f"\n--- Registrando pagamento para Aluno ID: {aluno_id} ---")
        new_payment_df = pd.DataFrame([{
            'aluno_id': aluno_id,
            'data_pagamento': datetime.datetime.now(),
            'valor_pago': valor_pago,
            'metodo_pagamento': metodo_pagamento,
            'referencia_aula_id': referencia_aula_id,
            'status': 'Pago',
            'observacoes': observacoes
        }])
        self.data_handler.insert_data_into_db('pagamentos', new_payment_df)
        print(f"Pagamento de R${valor_pago:.2f} registrado para o Aluno ID {aluno_id}.")

    def run_all_analysis(self, year='2024'):
        """
        Executa todas as análises disponíveis no sistema.
        """
        print(f"\n======== Executando Análises para o ano {year} ========")
        self.alunos_analyser.run_all_analysis(year)
        self.aulas_analyser.run_all_analysis(year)
        self.financeiro_analyser.run_all_analysis(year)
        self.professores_analyser.run_all_analysis(year)
        print("\n======== Análises Concluídas ========")

    def get_all_alunos(self):
        """Retorna todos os alunos."""
        return self.data_handler.fetch_data_from_db('alunos')

    def get_all_professores(self):
        """Retorna todos os professores."""
        return self.data_handler.fetch_data_from_db('professores')

    def get_all_instrumentos(self):
        """Retorna todos os instrumentos."""
        return self.data_handler.fetch_data_from_db('instrumentos')

    def get_all_aulas_ofertadas(self):
        """Retorna todas as aulas ofertadas."""
        return self.data_handler.fetch_data_from_db('aulas_ofertadas')

    def get_agenda_aulas(self, year='2024'):
        """Retorna a agenda de aulas para um dado ano."""
        # Note: A data_handler.fetch_data_from_db precisa de uma condição SQL para o ano.
        # Ou, idealmente, a tabela agenda_aulas armazenaria o ano diretamente, ou faremos um filtro aqui.
        return self.data_handler.fetch_data_from_db('agenda_aulas', condition=f"strftime('%Y', data_aula) = '{year}'")

# Função principal para executar o aplicativo
if __name__ == "__main__":
    app = AcademiaMaestroApp()

    # 1. Configurar o banco de dados (somente na primeira execução ou se o DB for resetado)
    # Crie as pastas data/2024 e coloque CSVs de exemplo se quiser testar a migração.
    # Caso contrário, o DB será criado e populado apenas com os seeds SQL.
    app.setup_database(years=['2024']) # Pode adicionar mais anos

    # 2. Exemplo de operações de CRUD e agendamento
    print("\n--- Exemplos de Operações ---")

    # Adicionar um novo aluno
    app.add_new_aluno("Gabriela Pereira", "1995-03-10", "Feminino", "gabriela.pereira@email.com", "11912345678")

    # Adicionar um professor (se não estiver no seed)
    # app.data_handler.insert_data_into_db('professores', pd.DataFrame([{'nome': 'Novo Prof', 'email': 'novo.prof@maestro.com', 'telefone': '11900000000', 'especializacao': 'Violão'}]))

    # Buscar IDs de exemplo (assumindo que já existem ou foram criados pelos seeds/testes)
    alunos_df = app.get_all_alunos()
    professores_df = app.get_all_professores()
    instrumentos_df = app.get_all_instrumentos()

    aluno_gabi_id = alunos_df[alunos_df['email'] == 'gabriela.pereira@email.com']['id'].iloc[0] if not alunos_df[alunos_df['email'] == 'gabriela.pereira@email.com'].empty else 1
    prof_ana_id = professores_df[professores_df['nome'] == 'Ana Silva']['id'].iloc[0] if not professores_df[professores_df['nome'] == 'Ana Silva'].empty else 1
    violao_id = instrumentos_df[instrumentos_df['nome_instrumento'] == 'Violão']['id'].iloc[0] if not instrumentos_df[instrumentos_df['nome_instrumento'] == 'Violão'].empty else 1
    teclado_id = instrumentos_df[instrumentos_df['nome_instrumento'] == 'Teclado']['id'].iloc[0] if not instrumentos_df[instrumentos_df['nome_instrumento'] == 'Teclado'].empty else 2


    # Agendar aulas
    app.schedule_aula(aluno_gabi_id, prof_ana_id, violao_id, '2024-07-20', '10:00', '11:00')
    app.schedule_aula(aluno_gabi_id, prof_ana_id, teclado_id, '2024-07-20', '11:00', '12:00') # Exemplo com outro instrumento

    # Registrar pagamento de uma aula (vamos assumir o ID da última aula agendada)
    # Para um sistema real, você obteria o ID da aula recém-agendada de forma mais robusta.
    agenda_aulas_df = app.data_handler.fetch_data_from_db('agenda_aulas', condition="aluno_id = " + str(aluno_gabi_id) + " ORDER BY id DESC LIMIT 1")
    if not agenda_aulas_df.empty:
        ultima_aula_id = agenda_aulas_df['id'].iloc[0]
        app.register_payment(aluno_gabi_id, 250.00, 'Pix', ultima_aula_id)

    # 3. Executar todas as análises
    app.run_all_analysis(year='2024')

    print("\nAplicação Academia Maestro encerrada.")