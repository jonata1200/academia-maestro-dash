# analysis/financeiro_analysis.py
import pandas as pd

class FinanceiroAnalysis:
    def __init__(self, data_handler):
        self.handler = data_handler

    def _filter_pagamentos_by_date(self, start_date, end_date):
        df_pagamentos = self.handler.get_data('pagamentos')
        if df_pagamentos.empty:
            return pd.DataFrame()
        
        df_pagamentos['data_pagamento'] = pd.to_datetime(df_pagamentos['data_pagamento'], errors='coerce')
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt = pd.to_datetime(end_date)

        mask = (df_pagamentos['data_pagamento'] >= start_date_dt) & (df_pagamentos['data_pagamento'] <= end_date_dt) & (df_pagamentos['status'] == 'Pago')
        return df_pagamentos.loc[mask]

    def get_faturamento_total_por_mes(self, start_date, end_date):
        pagamentos_validos = self._filter_pagamentos_by_date(start_date, end_date)
        if pagamentos_validos.empty:
            return pd.DataFrame(columns=['mes', 'faturamento_mensal'])
        
        pagamentos_validos['mes'] = pagamentos_validos['data_pagamento'].dt.strftime('%Y-%m')
        resultado = pagamentos_validos.groupby('mes')['valor_pago'].sum().reset_index(name='faturamento_mensal')
        return resultado.sort_values('mes')

    def get_faturamento_por_instrumento(self, start_date, end_date):
        pagamentos_validos = self._filter_pagamentos_by_date(start_date, end_date)
        df_agenda = self.handler.get_data('agenda_aulas')
        df_instrumentos = self.handler.get_data('instrumentos')
        if pagamentos_validos.empty or df_agenda.empty or df_instrumentos.empty:
            return pd.DataFrame()

        merge1 = pd.merge(pagamentos_validos, df_agenda, left_on='referencia_aula_id', right_on='id')
        merge2 = pd.merge(merge1, df_instrumentos, left_on='instrumento_id', right_on='id')
        resultado = merge2.groupby('nome_instrumento')['valor_pago'].sum().reset_index(name='faturamento_instrumento')
        return resultado.sort_values('faturamento_instrumento', ascending=False)

    def get_faturamento_por_professor(self, start_date, end_date):
        pagamentos_validos = self._filter_pagamentos_by_date(start_date, end_date)
        df_agenda = self.handler.get_data('agenda_aulas')
        df_professores = self.handler.get_data('professores')
        if pagamentos_validos.empty or df_agenda.empty or df_professores.empty:
            return pd.DataFrame()
        
        merge1 = pd.merge(pagamentos_validos, df_agenda, left_on='referencia_aula_id', right_on='id')
        merge2 = pd.merge(merge1, df_professores, left_on='professor_id', right_on='id')
        resultado = merge2.groupby('nome')['valor_pago'].sum().reset_index(name='faturamento_professor')
        resultado = resultado.rename(columns={'nome': 'nome_professor'})
        return resultado.sort_values('faturamento_professor', ascending=False)