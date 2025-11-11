import pandas as pd
from sqlalchemy import create_engine
from config.settings import DATABASE_PATH

class FinanceiroAnalysis:
    def __init__(self, db_path=DATABASE_PATH):
        """
        Inicializa a classe de análise financeira, conectando ao banco de dados.
        """
        self.engine = create_engine(f'sqlite:///{db_path}')
        print(f"Conectado ao banco de dados em: {db_path}")

    def get_faturamento_total_por_mes(self, ano):
        """
        Calcula o faturamento total por mês (considerando pagamentos concluídos).
        """
        query = f"""
        SELECT
            strftime('%Y-%m', data_pagamento) AS mes,
            SUM(valor_pago) AS faturamento_mensal
        FROM pagamentos
        WHERE strftime('%Y', data_pagamento) = '{ano}' AND status = 'Pago'
        GROUP BY mes
        ORDER BY mes;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_faturamento_por_instrumento(self, ano):
        """
        Calcula o faturamento gerado por cada tipo de instrumento (aula).
        Assume que o pagamento está ligado à agenda_aulas e que a agenda_aulas
        tem o instrumento_id.
        """
        query = f"""
        SELECT
            i.nome_instrumento,
            SUM(p.valor_pago) AS faturamento_instrumento
        FROM pagamentos p
        JOIN agenda_aulas aa ON p.referencia_aula_id = aa.id -- Assumindo 1 pagamento por aula agendada
        JOIN instrumentos i ON aa.instrumento_id = i.id
        WHERE strftime('%Y', p.data_pagamento) = '{ano}' AND p.status = 'Pago'
        GROUP BY i.nome_instrumento
        ORDER BY faturamento_instrumento DESC;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_top_alunos_faturamento(self, top_n=5, ano='2024'):
        """
        Retorna os alunos que mais contribuíram para o faturamento.
        """
        query = f"""
        SELECT
            a.nome AS nome_aluno,
            SUM(p.valor_pago) AS total_gasto
        FROM pagamentos p
        JOIN alunos a ON p.aluno_id = a.id
        WHERE strftime('%Y', p.data_pagamento) = '{ano}' AND p.status = 'Pago'
        GROUP BY a.nome
        ORDER BY total_gasto DESC
        LIMIT {top_n};
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df

    def get_faturamento_por_professor(self, ano='2024'):
        """
        Calcula o faturamento (receita bruta) gerado por cada professor.
        Assume que o pagamento está ligado à agenda_aulas, que tem o professor_id.
        """
        query = f"""
        SELECT
            pr.nome AS nome_professor,
            SUM(p.valor_pago) AS faturamento_professor
        FROM pagamentos p
        JOIN agenda_aulas aa ON p.referencia_aula_id = aa.id
        JOIN professores pr ON aa.professor_id = pr.id
        WHERE strftime('%Y', p.data_pagamento) = '{ano}' AND p.status = 'Pago'
        GROUP BY pr.nome
        ORDER BY faturamento_professor DESC;
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df


    def run_all_analysis(self, ano_referencia='2024'):
        """
        Executa todas as análises financeiras e imprime os resultados.
        """
        print("\n--- Análise Financeira ---")

        faturamento_mensal = self.get_faturamento_total_por_mes(ano_referencia)
        print(f"\nFaturamento total por mês ({ano_referencia}):")
        print(faturamento_mensal)

        faturamento_instrumento = self.get_faturamento_por_instrumento(ano_referencia)
        print(f"\nFaturamento por instrumento ({ano_referencia}):")
        print(faturamento_instrumento)

        top_alunos = self.get_top_alunos_faturamento(ano=ano_referencia)
        print(f"\nTop 5 alunos por faturamento ({ano_referencia}):")
        print(top_alunos)

        faturamento_professor = self.get_faturamento_por_professor(ano=ano_referencia)
        print(f"\nFaturamento gerado por professor ({ano_referencia}):")
        print(faturamento_professor)


# Exemplo de uso:
if __name__ == "__main__":
    try:
        from config.settings import DATABASE_PATH
    except ImportError:
        print("Erro: config/settings.py não encontrado ou DATABASE_PATH não definido.")
        print("Por favor, crie config/settings.py com 'DATABASE_PATH = \"db/maestro.db\"'")
        exit()

    analisador = FinanceiroAnalysis()
    analisador.run_all_analysis(ano_referencia='2024')