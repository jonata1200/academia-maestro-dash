# analysis/aulas_analysis.py

import pandas as pd

class AulasAnalysis:
    def __init__(self, data_handler):
        """
        Inicializa a classe de análise de aulas, recebendo o DataHandler.
        """
        self.handler = data_handler
        print("Analisador de Aulas (Modo Pandas) inicializado.")

    def get_total_aulas_por_status(self, ano):
        """
        Retorna o total de aulas agendadas por status (Agendada, Concluída, Cancelada) para um dado ano.
        Lógica SQL: SELECT status, COUNT(id) FROM agenda_aulas WHERE YEAR(data_aula) = ano GROUP BY status.
        """
        df_agenda = self.handler.get_data('agenda_aulas')
        if df_agenda.empty:
            return pd.DataFrame(columns=['status', 'total_aulas'])

        # Garante que a coluna de data é do tipo datetime
        df_agenda['data_aula'] = pd.to_datetime(df_agenda['data_aula'])
        
        # 1. Filtra o DataFrame pelo ano desejado
        df_ano = df_agenda[df_agenda['data_aula'].dt.year == int(ano)]
        
        # 2. Agrupa por 'status' e conta o número de ocorrências
        resultado = df_ano.groupby('status').size().reset_index(name='total_aulas')
        
        return resultado

    def get_popularidade_instrumentos(self):
        """
        Retorna a popularidade dos instrumentos com base no número de aulas agendadas.
        Lógica SQL: SELECT i.nome_instrumento, COUNT(aa.id) FROM agenda_aulas aa JOIN instrumentos i ON aa.instrumento_id = i.id GROUP BY i.nome_instrumento.
        """
        df_agenda = self.handler.get_data('agenda_aulas')
        df_instrumentos = self.handler.get_data('instrumentos')

        if df_agenda.empty or df_instrumentos.empty:
            return pd.DataFrame(columns=['nome_instrumento', 'total_aulas_agendadas'])

        # 1. Junta (merge) os dois DataFrames
        df_merged = pd.merge(df_agenda, df_instrumentos, left_on='instrumento_id', right_on='id')

        # 2. Agrupa pelo nome do instrumento e conta as aulas
        resultado = df_merged.groupby('nome_instrumento').size().reset_index(name='total_aulas_agendadas')
        
        # 3. Ordena do mais popular para o menos popular
        return resultado.sort_values('total_aulas_agendadas', ascending=False)

    def get_aulas_por_professor(self, ano):
        """
        Retorna o número de aulas concluídas por professor para um dado ano.
        Lógica SQL: SELECT p.nome, COUNT(aa.id) FROM agenda_aulas aa JOIN professores p ON ... WHERE aa.status = 'Concluída' AND YEAR(data_aula) = ano GROUP BY p.nome.
        """
        df_agenda = self.handler.get_data('agenda_aulas')
        df_professores = self.handler.get_data('professores')

        if df_agenda.empty or df_professores.empty:
            return pd.DataFrame(columns=['nome_professor', 'aulas_concluidas'])

        df_agenda['data_aula'] = pd.to_datetime(df_agenda['data_aula'])
        
        # 1. Filtra a agenda por aulas 'Concluída' e pelo ano
        filtro = (df_agenda['status'] == 'Concluída') & (df_agenda['data_aula'].dt.year == int(ano))
        df_agenda_filtrada = df_agenda[filtro]

        # 2. Junta com o DataFrame de professores
        df_merged = pd.merge(df_agenda_filtrada, df_professores, left_on='professor_id', right_on='id')
        
        # 3. Agrupa pelo nome do professor e conta as aulas
        resultado = df_merged.groupby('nome').size().reset_index(name='aulas_concluidas')
        resultado = resultado.rename(columns={'nome': 'nome_professor'})
        
        return resultado.sort_values('aulas_concluidas', ascending=False)

    def get_ocupacao_horarios_professor(self, professor_id=None, ano='2024'):
        """
        Analisa a ocupação de horários, contando a média de aulas por dia útil.
        """
        df_agenda = self.handler.get_data('agenda_aulas')
        if df_agenda.empty:
            return 0

        df_agenda['data_aula'] = pd.to_datetime(df_agenda['data_aula'])
        
        # 1. Filtra por ano
        df_filtrada = df_agenda[df_agenda['data_aula'].dt.year == int(ano)]
        
        # 2. Filtro opcional por professor
        if professor_id:
            df_filtrada = df_filtrada[df_filtrada['professor_id'] == int(professor_id)]

        if df_filtrada.empty:
            return 0
            
        # 3. Conta aulas por dia
        aulas_por_dia = df_filtrada.groupby(df_filtrada['data_aula'].dt.date).size()
        
        # 4. Calcula a média
        media_aulas_dia = aulas_por_dia.mean()
        
        return media_aulas_dia if pd.notna(media_aulas_dia) else 0