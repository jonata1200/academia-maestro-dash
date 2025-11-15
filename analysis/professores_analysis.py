# analysis/professores_analysis.py

import pandas as pd

class ProfessoresAnalysis:
    def __init__(self, data_handler):
        self.handler = data_handler

    # --- FUNÇÃO ATUALIZADA E MELHORADA ---
    def get_carga_horaria_professor(self, start_date, end_date):
        """
        Calcula a carga horária (em aulas e horas) por professor para um dado período.
        """
        df_agenda = self.handler.get_data('agenda_aulas')
        df_professores = self.handler.get_data('professores')

        if df_agenda.empty or df_professores.empty:
            return pd.DataFrame(columns=['nome_professor', 'aulas_concluidas', 'horas_lecionadas'])

        # Prepara as colunas de data e hora
        df_agenda['data_aula'] = pd.to_datetime(df_agenda['data_aula'], errors='coerce')
        df_agenda['hora_inicio'] = pd.to_timedelta(df_agenda['hora_inicio'].astype(str), errors='coerce')
        df_agenda['hora_fim'] = pd.to_timedelta(df_agenda['hora_fim'].astype(str), errors='coerce')

        # Filtra pelo período e status
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt = pd.to_datetime(end_date)
        mask = (
            (df_agenda['status'] == 'Concluída') &
            (df_agenda['data_aula'] >= start_date_dt) &
            (df_agenda['data_aula'] <= end_date_dt)
        )
        df_agenda_filtrada = df_agenda.loc[mask].copy()

        if df_agenda_filtrada.empty:
            return pd.DataFrame(columns=['nome_professor', 'aulas_concluidas', 'horas_lecionadas'])
            
        # Calcula a duração de cada aula em horas
        df_agenda_filtrada['duracao_horas'] = (df_agenda_filtrada['hora_fim'] - df_agenda_filtrada['hora_inicio']).dt.total_seconds() / 3600

        # Junta com a tabela de professores
        df_merged = pd.merge(df_agenda_filtrada, df_professores, left_on='professor_id', right_on='id')

        # Agrupa por nome e agrega os resultados
        resultado = df_merged.groupby('nome').agg(
            aulas_concluidas=('id_x', 'count'),
            horas_lecionadas=('duracao_horas', 'sum')
        ).reset_index()
        resultado = resultado.rename(columns={'nome': 'nome_professor'})
        
        return resultado.sort_values('aulas_concluidas', ascending=False)

    def get_instrumentos_por_professor(self):
        # (Este método não precisa de alteração)
        df_agenda = self.handler.get_data('agenda_aulas')
        df_professores = self.handler.get_data('professores')
        df_instrumentos = self.handler.get_data('instrumentos')

        if df_agenda.empty or df_professores.empty or df_instrumentos.empty:
            return pd.DataFrame()
            
        aulas_concluidas = df_agenda[df_agenda['status'] == 'Concluída']
        merge1 = pd.merge(aulas_concluidas, df_professores, left_on='professor_id', right_on='id')
        merge2 = pd.merge(merge1, df_instrumentos, left_on='instrumento_id', right_on='id', suffixes=('_prof', '_instr'))
        
        resultado = merge2.groupby('nome').agg(
            instrumentos_lecionados=('nome_instrumento', lambda x: ', '.join(x.unique()))
        ).reset_index()
        resultado = resultado.rename(columns={'nome': 'nome_professor'})
        
        return resultado.sort_values('nome_professor')