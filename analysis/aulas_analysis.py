# analysis/aulas_analysis.py
import pandas as pd

class AulasAnalysis:
    def __init__(self, data_handler):
        self.handler = data_handler

    def _filter_aulas_by_date(self, start_date, end_date, status_filter=None):
        df_agenda = self.handler.get_data('agenda_aulas')
        if df_agenda.empty:
            return pd.DataFrame()
        
        df_agenda['data_aula'] = pd.to_datetime(df_agenda['data_aula'], errors='coerce')
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt = pd.to_datetime(end_date)
        
        mask = (df_agenda['data_aula'] >= start_date_dt) & (df_agenda['data_aula'] <= end_date_dt)
        df_periodo = df_agenda.loc[mask]
        
        if status_filter and not df_periodo.empty:
            df_periodo = df_periodo[df_periodo['status'].isin(status_filter)]
            
        return df_periodo

    def get_total_aulas_por_status(self, start_date, end_date):
        df_periodo = self._filter_aulas_by_date(start_date, end_date)
        if df_periodo.empty:
            return pd.DataFrame(columns=['status', 'total_aulas'])
        return df_periodo.groupby('status').size().reset_index(name='total_aulas')

    def get_popularidade_instrumentos(self, start_date, end_date):
        df_periodo = self._filter_aulas_by_date(start_date, end_date)
        df_instrumentos = self.handler.get_data('instrumentos')
        if df_periodo.empty or df_instrumentos.empty:
            return pd.DataFrame()
        
        df_merged = pd.merge(df_periodo, df_instrumentos, left_on='instrumento_id', right_on='id')
        resultado = df_merged.groupby('nome_instrumento').size().reset_index(name='total_aulas_agendadas')
        return resultado.sort_values('total_aulas_agendadas', ascending=False)

    def get_peak_hours_data(self, start_date, end_date):
        # (Este método já está correto)
        df_periodo = self._filter_aulas_by_date(start_date, end_date)
        if df_periodo.empty:
            return pd.DataFrame()
        # ... resto do código ...
        df_periodo['dia_semana_num'] = df_periodo['data_aula'].dt.weekday
        df_periodo['dia_semana_nome'] = df_periodo['data_aula'].dt.day_name(locale='pt_BR.utf8')
        df_periodo['hora_aula'] = pd.to_datetime(df_periodo['hora_inicio'], format='%H:%M:%S', errors='coerce').dt.hour
        heatmap_data = df_periodo.pivot_table(index=['dia_semana_num', 'dia_semana_nome'], columns='hora_aula', values='id', aggfunc='count', fill_value=0)
        dias_ordem = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
        heatmap_data = heatmap_data.reset_index().set_index('dia_semana_num').rename(columns={'dia_semana_nome':''}).reindex(range(7)).fillna(0)
        heatmap_data[''] = heatmap_data.index.map(dias_ordem)
        heatmap_data = heatmap_data.set_index('')
        return heatmap_data