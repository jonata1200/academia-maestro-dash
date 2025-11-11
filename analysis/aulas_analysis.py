import pandas as pd
from sqlalchemy import create_engine
from config.settings import DATABASE_PATH

class AulasAnalysis:
    def __init__(self, db_path=DATABASE_PATH):
        """
        Inicializa a classe de análise de aulas, conectando ao banco de dados.
        """
        self.engine = create_engine(f'sqlite:///{db_path}')
        print(f"Conectado ao banco de dados em: {db_path}")

    def get_total_aulas_por_status(self, ano):
        """
        Retorna o total de aulas agendadas por status (Agendada, Concluída, Cancelada) para um dado ano.
        """
        query = f"""
        SELECT
            status,
            COUNT(id) AS total_aulas
        FROM agenda_aulas
        WHERE strftime('%Y', data_aula) = '{ano}'
        GROUP BY status;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_popularidade_instrumentos(self):
        """
        Retorna a popularidade dos instrumentos com base no número de aulas agendadas.
        """
        query = """
        SELECT
            i.nome_instrumento,
            COUNT(aa.id) AS total_aulas_agendadas
        FROM agenda_aulas aa
        JOIN instrumentos i ON aa.instrumento_id = i.id
        GROUP BY i.nome_instrumento
        ORDER BY total_aulas_agendadas DESC;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_aulas_por_professor(self, ano):
        """
        Retorna o número de aulas concluídas por professor para um dado ano.
        """
        query = f"""
        SELECT
            p.nome AS nome_professor,
            COUNT(aa.id) AS aulas_concluidas
        FROM agenda_aulas aa
        JOIN professores p ON aa.professor_id = p.id
        WHERE aa.status = 'Concluída' AND strftime('%Y', data_aula) = '{ano}'
        GROUP BY p.nome
        ORDER BY aulas_concluidas DESC;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_ocupacao_horarios_professor(self, professor_id=None, ano='2024'):
        """
        Analisa a ocupação de horários. Para simplificar, conta a média de aulas por dia útil.
        Pode ser expandido para analisar slots específicos.
        """
        base_query = f"""
        SELECT
            strftime('%Y-%m-%d', data_aula) AS dia,
            COUNT(id) AS aulas_no_dia
        FROM agenda_aulas
        WHERE strftime('%Y', data_aula) = '{ano}'
        """
        if professor_id:
            base_query += f" AND professor_id = {professor_id}"
        base_query += " GROUP BY dia ORDER BY dia;"

        with self.engine.connect() as connection:
            df = pd.read_sql(base_query, connection)

        if not df.empty:
            media_aulas_dia = df['aulas_no_dia'].mean()
            return media_aulas_dia
        return 0

    def run_all_analysis(self, ano_referencia='2024'):
        """
        Executa todas as análises de aulas e imprime os resultados.
        """
        print("\n--- Análise de Aulas ---")

        total_aulas_status = self.get_total_aulas_por_status(ano_referencia)
        print(f"\nTotal de aulas por status ({ano_referencia}):")
        print(total_aulas_status)

        popularidade_instr = self.get_popularidade_instrumentos()
        print("\nPopularidade dos instrumentos (por aulas agendadas):")
        print(popularidade_instr)

        aulas_prof = self.get_aulas_por_professor(ano_referencia)
        print(f"\nAulas concluídas por professor ({ano_referencia}):")
        print(aulas_prof)

        ocupacao_geral = self.get_ocupacao_horarios_professor(ano=ano_referencia)
        print(f"\nMédia de aulas por dia com agendamentos em {ano_referencia}: {ocupacao_geral:.2f}")

# Exemplo de uso:
if __name__ == "__main__":
    try:
        from config.settings import DATABASE_PATH
    except ImportError:
        print("Erro: config/settings.py não encontrado ou DATABASE_PATH não definido.")
        print("Por favor, crie config/settings.py com 'DATABASE_PATH = \"db/maestro.db\"'")
        exit()

    analisador = AulasAnalysis()
    analisador.run_all_analysis(ano_referencia='2024')