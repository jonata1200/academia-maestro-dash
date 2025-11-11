# analysis/professores_analysis.py

import pandas as pd

class ProfessoresAnalysis:
    def __init__(self, data_handler):
        """
        Inicializa a classe de análise de professores, recebendo o DataHandler.
        """
        self.handler = data_handler
        print("Analisador de Professores (Modo Pandas) inicializado.")

    def get_carga_horaria_professor(self, ano):
        """
        Calcula a carga horária (em número de aulas e horas) por professor para um dado ano.
        """
        df_agenda = self.handler.get_data('agenda_aulas')
        df_professores = self.handler.get_data('professores')

        if df_agenda.empty or df_professores.empty:
            return pd.DataFrame()

        # 1. Converte tipos e filtra dados relevantes
        df_agenda['data_aula'] = pd.to_datetime(df_agenda['data_aula'])
        filtro = (df_agenda['status'] == 'Concluída') & (df_agenda['data_aula'].dt.year == int(ano))
        df_agenda_filtrada = df_agenda[filtro].copy()

        if df_agenda_filtrada.empty:
            return pd.DataFrame()
            
        # 2. Calcula a duração de cada aula em horas
        # As horas podem ser strings, então convertemos para timedelta para subtrair
        hora_inicio = pd.to_timedelta(df_agenda_filtrada['hora_inicio'].astype(str))
        hora_fim = pd.to_timedelta(df_agenda_filtrada['hora_fim'].astype(str))
        df_agenda_filtrada['duracao_horas'] = (hora_fim - hora_inicio).dt.total_seconds() / 3600

        # 3. Junta com professores
        df_merged = pd.merge(df_agenda_filtrada, df_professores, left_on='professor_id', right_on='id')

        # 4. Agrupa por nome e agrega os resultados (conta aulas e soma horas)
        resultado = df_merged.groupby('nome').agg(
            aulas_concluidas=('id', 'count'),
            horas_lecionadas=('duracao_horas', 'sum')
        ).reset_index()
        resultado = resultado.rename(columns={'nome': 'nome_professor'})
        
        return resultado.sort_values('aulas_concluidas', ascending=False)


    def get_instrumentos_por_professor(self):
        """
        Lista os instrumentos que cada professor leciona.
        Lógica SQL: ... GROUP_CONCAT(DISTINCT i.nome_instrumento) ...
        """
        df_agenda = self.handler.get_data('agenda_aulas')
        df_professores = self.handler.get_data('professores')
        df_instrumentos = self.handler.get_data('instrumentos')

        if df_agenda.empty or df_professores.empty or df_instrumentos.empty:
            return pd.DataFrame()

        # 1. Filtra aulas concluídas para ter uma base de dados real
        aulas_concluidas = df_agenda[df_agenda['status'] == 'Concluída']
        
        # 2. Junta as três tabelas
        merge1 = pd.merge(aulas_concluidas, df_professores, left_on='professor_id', right_on='id')
        merge2 = pd.merge(merge1, df_instrumentos, left_on='instrumento_id', right_on='id', suffixes=('_prof', '_instr'))
        
        # 3. Agrupa e aplica uma função para obter instrumentos únicos e juntá-los em uma string
        resultado = merge2.groupby('nome').agg(
            instrumentos_lecionados=('nome_instrumento', lambda x: ', '.join(x.unique()))
        ).reset_index()
        resultado = resultado.rename(columns={'nome': 'nome_professor'})
        
        return resultado.sort_values('nome_professor')


    def get_disponibilidade_professor(self, professor_id, data_inicio, data_fim):
        """
        Retorna os horários ocupados de um professor em um período.
        """
        df_agenda = self.handler.get_data('agenda_aulas')
        if df_agenda.empty:
            return pd.DataFrame()

        df_agenda['data_aula'] = pd.to_datetime(df_agenda['data_aula']).dt.date

        # 1. Converte as datas de string para date para comparação
        data_inicio_obj = pd.to_datetime(data_inicio).date()
        data_fim_obj = pd.to_datetime(data_fim).date()

        # 2. Aplica todos os filtros
        filtro = (
            (df_agenda['professor_id'] == int(professor_id)) &
            (df_agenda['data_aula'] >= data_inicio_obj) &
            (df_agenda['data_aula'] <= data_fim_obj) &
            (df_agenda['status'].isin(['Agendada', 'Concluída']))
        )
        resultado = df_agenda[filtro]
        
        # 3. Seleciona as colunas de interesse e ordena
        colunas_finais = ['data_aula', 'hora_inicio', 'hora_fim']
        return resultado[colunas_finais].sort_values(by=['data_aula', 'hora_inicio'])