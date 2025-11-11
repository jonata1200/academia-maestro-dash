import pandas as pd
from sqlalchemy import create_engine
from config.settings import DATABASE_PATH

class AlunosAnalysis:
    def __init__(self, db_path=DATABASE_PATH):
        """
        Inicializa a classe de análise de alunos, conectando ao banco de dados.
        """
        self.engine = create_engine(f'sqlite:///{db_path}')
        print(f"Conectado ao banco de dados em: {db_path}")

    def get_total_alunos(self, status='Ativo'):
        """
        Retorna o número total de alunos com um determinado status.
        """
        query = f"SELECT COUNT(DISTINCT id) FROM alunos WHERE status = '{status}'"
        with self.engine.connect() as connection:
            total_alunos = pd.read_sql(query, connection).iloc[0, 0]
        return total_alunos

    def get_novas_matriculas_por_mes(self, ano):
        """
        Retorna o número de novas matrículas por mês para um dado ano.
        """
        query = f"""
        SELECT
            strftime('%Y-%m', data_matricula) AS mes,
            COUNT(id) AS novas_matriculas
        FROM matriculas
        WHERE strftime('%Y', data_matricula) = '{ano}'
        GROUP BY mes
        ORDER BY mes;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_alunos_por_instrumento(self):
        """
        Retorna a contagem de alunos matriculados por instrumento.
        """
        query = """
        SELECT
            i.nome_instrumento,
            COUNT(DISTINCT m.aluno_id) AS total_alunos
        FROM matriculas m
        JOIN aulas_ofertadas ao ON m.aula_ofertada_id = ao.id
        JOIN instrumentos i ON ao.instrumento_id = i.id
        WHERE m.status = 'Ativa'
        GROUP BY i.nome_instrumento
        ORDER BY total_alunos DESC;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_alunos_com_pagamento_pendente(self):
        """
        Retorna uma lista de alunos com pagamentos pendentes.
        Isso assume que 'pagamentos' tem uma coluna 'status' e 'agenda_aulas' tem 'valor_aula'.
        É uma lógica mais complexa e pode precisar de ajustes dependendo de como você gerencia pacotes.
        Por simplicidade, vamos considerar aulas agendadas que não possuem pagamento associado.
        """
        query = """
        SELECT
            a.nome AS nome_aluno,
            a.email AS email_aluno,
            aa.data_aula,
            aa.hora_inicio,
            aa.valor_aula
        FROM agenda_aulas aa
        JOIN alunos a ON aa.aluno_id = a.id
        LEFT JOIN pagamentos p ON aa.id = p.referencia_aula_id AND p.status = 'Pago'
        WHERE aa.status = 'Concluída' AND p.id IS NULL;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def run_all_analysis(self, ano_referencia='2024'):
        """
        Executa todas as análises de alunos e imprime os resultados.
        """
        print("\n--- Análise de Alunos ---")

        total_ativos = self.get_total_alunos(status='Ativo')
        print(f"Total de alunos ativos: {total_ativos}")

        novas_matriculas = self.get_novas_matriculas_por_mes(ano_referencia)
        print(f"\nNovas matrículas por mês ({ano_referencia}):")
        print(novas_matriculas)

        alunos_por_instr = self.get_alunos_por_instrumento()
        print("\nAlunos ativos por instrumento:")
        print(alunos_por_instr)

        alunos_pendentes = self.get_alunos_com_pagamento_pendente()
        if not alunos_pendentes.empty:
            print("\nAlunos com aulas concluídas e pagamentos pendentes:")
            print(alunos_pendentes)
        else:
            print("\nNenhum aluno com aulas concluídas e pagamentos pendentes encontrado.")

# Exemplo de uso:
if __name__ == "__main__":
    # É importante que o DATABASE_PATH em config.settings esteja configurado
    # e que o banco de dados e tabelas já existam com dados de exemplo.
    # Para rodar este script isoladamente, garanta que o path do projeto esteja no PYTHONPATH
    # ou execute a partir da raiz do projeto: python analysis/alunos_analysis.py

    # Criar um arquivo config/settings.py para que isso funcione
    try:
        from config.settings import DATABASE_PATH
    except ImportError:
        print("Erro: config/settings.py não encontrado ou DATABASE_PATH não definido.")
        print("Por favor, crie config/settings.py com 'DATABASE_PATH = \"db/maestro.db\"'")
        exit()

    analisador = AlunosAnalysis()
    analisador.run_all_analysis(ano_referencia='2024')