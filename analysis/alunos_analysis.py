import pandas as pd

class AlunosAnalysis:
    def __init__(self, data_handler):
        """Inicializa a classe de análise, recebendo o DataHandler."""
        self.handler = data_handler

    def get_total_alunos(self, status='Ativo'):
        """Retorna o número total de alunos com um determinado status."""
        df_alunos = self.handler.get_data('alunos')
        if df_alunos.empty:
            return 0
        return df_alunos[df_alunos['status'] == status].shape[0]

    def get_novas_matriculas_por_mes(self, ano):
        """Retorna o número de novas matrículas por mês para um dado ano."""
        df_matriculas = self.handler.get_data('matriculas')
        if df_matriculas.empty:
            return pd.DataFrame(columns=['mes', 'novas_matriculas'])
        
        # Converte a coluna para datetime e filtra pelo ano
        df_matriculas['data_matricula'] = pd.to_datetime(df_matriculas['data_matricula'])
        df_ano = df_matriculas[df_matriculas['data_matricula'].dt.year == int(ano)].copy()
        
        if df_ano.empty:
            return pd.DataFrame(columns=['mes', 'novas_matriculas'])

        # Agrupa por mês
        df_ano['mes'] = df_ano['data_matricula'].dt.strftime('%Y-%m')
        novas_matriculas = df_ano.groupby('mes').size().reset_index(name='novas_matriculas')
        return novas_matriculas.sort_values('mes')

    def get_alunos_por_instrumento(self):
        """Retorna a contagem de alunos matriculados por instrumento (exemplo com JOIN)."""
        df_matriculas = self.handler.get_data('matriculas')
        df_aulas = self.handler.get_data('aulas_ofertadas')
        df_instrumentos = self.handler.get_data('instrumentos')

        if df_matriculas.empty or df_aulas.empty or df_instrumentos.empty:
            return pd.DataFrame()

        # Simulando o JOIN com pd.merge
        matriculas_ativas = df_matriculas[df_matriculas['status'] == 'Ativa']
        merge1 = pd.merge(matriculas_ativas, df_aulas, left_on='aula_ofertada_id', right_on='id', suffixes=('', '_aula'))
        merge2 = pd.merge(merge1, df_instrumentos, left_on='instrumento_id', right_on='id', suffixes=('', '_instr'))

        # Agrupando e contando
        resultado = merge2.groupby('nome_instrumento')['aluno_id'].nunique().reset_index(name='total_alunos')
        return resultado.sort_values('total_alunos', ascending=False)
    
    # Adapte o `run_all_analysis` para retornar os dados, como sugerido anteriormente.