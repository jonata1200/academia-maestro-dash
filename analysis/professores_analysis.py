import pandas as pd
from sqlalchemy import create_engine
from config.settings import DATABASE_PATH

class ProfessoresAnalysis:
    def __init__(self, db_path=DATABASE_PATH):
        """
        Inicializa a classe de análise de professores, conectando ao banco de dados.
        """
        self.engine = create_engine(f'sqlite:///{db_path}')
        print(f"Conectado ao banco de dados em: {db_path}")

    def get_carga_horaria_professor(self, ano):
        """
        Calcula a carga horária (em número de aulas concluídas) por professor para um dado ano.
        """
        query = f"""
        SELECT
            p.nome AS nome_professor,
            COUNT(aa.id) AS aulas_concluidas,
            SUM(strftime('%J', aa.hora_fim) - strftime('%J', aa.hora_inicio)) * 24 AS horas_lecionadas_estimadas
            -- Esta estimativa pode não ser precisa para duração de aula, assume horas cheias.
            -- Idealmente, armazenar a duração da aula em minutos/horas.
        FROM agenda_aulas aa
        JOIN professores p ON aa.professor_id = p.id
        WHERE aa.status = 'Concluída' AND strftime('%Y', data_aula) = '{ano}'
        GROUP BY p.nome
        ORDER BY aulas_concluidas DESC;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_instrumentos_por_professor(self):
        """
        Lista os instrumentos que cada professor leciona.
        Assumimos uma tabela de `professores_instrumentos` ou inferimos das `agenda_aulas`.
        Vamos inferir das `agenda_aulas` por simplicidade, considerando aulas concluídas.
        """
        query = """
        SELECT
            p.nome AS nome_professor,
            GROUP_CONCAT(DISTINCT i.nome_instrumento) AS instrumentos_lecionados
        FROM agenda_aulas aa
        JOIN professores p ON aa.professor_id = p.id
        JOIN instrumentos i ON aa.instrumento_id = i.id
        WHERE aa.status = 'Concluída'
        GROUP BY p.nome
        ORDER BY p.nome;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_disponibilidade_professor(self, professor_id, data_inicio, data_fim):
        """
        Retorna os horários ocupados de um professor em um período,
        indicando sua "indisponibilidade".
        """
        query = f"""
        SELECT
            data_aula,
            hora_inicio,
            hora_fim
        FROM agenda_aulas
        WHERE professor_id = {professor_id}
          AND data_aula BETWEEN '{data_inicio}' AND '{data_fim}'
          AND status IN ('Agendada', 'Concluída')
        ORDER BY data_aula, hora_inicio;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def run_all_analysis(self, ano_referencia='2024'):
        """
        Executa todas as análises de professores e imprime os resultados.
        """
        print("\n--- Análise de Professores ---")

        carga_horaria = self.get_carga_horaria_professor(ano_referencia)
        print(f"\nCarga horária e aulas concluídas por professor ({ano_referencia}):")
        print(carga_horaria)

        instrumentos_prof = self.get_instrumentos_por_professor()
        print("\nInstrumentos lecionados por professor:")
        print(instrumentos_prof)

        # Exemplo de uso de disponibilidade (requer um professor_id e datas)
        # Supondo que você tem um professor com id=1 para testes
        # if not carga_horaria.empty:
        #     primeiro_professor_id = 1 # Substitua por um ID real ou pegue da lista
        #     print(f"\nDisponibilidade para o Professor ID {primeiro_professor_id} (Exemplo de 1 semana):")
        #     # Isso é um placeholder. Você precisaria de um professor_id real e datas
        #     # dispo = self.get_disponibilidade_professor(primeiro_professor_id, '2024-01-01', '2024-01-07')
        #     # print(dispo)
        # else:
        #     print("\nNão há professores com aulas concluídas para analisar disponibilidade.")


# Exemplo de uso:
if __name__ == "__main__":
    try:
        from config.settings import DATABASE_PATH
    except ImportError:
        print("Erro: config/settings.py não encontrado ou DATABASE_PATH não definido.")
        print("Por favor, crie config/settings.py com 'DATABASE_PATH = \"db/maestro.db\"'")
        exit()

    analisador = ProfessoresAnalysis()
    analisador.run_all_analysis(ano_referencia='2024')