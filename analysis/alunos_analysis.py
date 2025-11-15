# analysis/alunos_analysis.py

import pandas as pd

class AlunosAnalysis:
    def __init__(self, data_handler):
        self.handler = data_handler

    def get_total_alunos(self, status='Ativo'):
        df_alunos = self.handler.get_data('alunos')
        if df_alunos.empty:
            return 0
        return df_alunos[df_alunos['status'] == status].shape[0]

    def get_novas_matriculas_por_mes(self, start_date, end_date):
        # (Este método continua o mesmo)
        df_alunos = self.handler.get_data('alunos')
        if df_alunos.empty or 'data_cadastro' not in df_alunos.columns:
            return pd.DataFrame(columns=['mes', 'novas_matriculas'])
        df_alunos['data_cadastro'] = pd.to_datetime(df_alunos['data_cadastro'], errors='coerce')
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt = pd.to_datetime(end_date)
        mask = (df_alunos['data_cadastro'] >= start_date_dt) & (df_alunos['data_cadastro'] <= end_date_dt)
        df_periodo = df_alunos.loc[mask].copy()
        if df_periodo.empty:
            return pd.DataFrame(columns=['mes', 'novas_matriculas'])
        df_periodo['mes'] = df_periodo['data_cadastro'].dt.strftime('%Y-%m')
        novas_matriculas = df_periodo.groupby('mes').size().reset_index(name='novas_matriculas')
        return novas_matriculas.sort_values('mes')

    # --- NOVA FUNÇÃO ADICIONADA ---
    def get_churn_kpis(self):
        """
        Calcula a taxa de evasão geral (lifetime).
        Retorna um dicionário com o total de alunos inativos e a taxa de evasão.
        """
        df_alunos = self.handler.get_data('alunos')
        if df_alunos.empty:
            return {"inativos": 0, "taxa_evasao": 0.0}

        total_alunos = len(df_alunos)
        alunos_inativos = len(df_alunos[df_alunos['status'] == 'Inativo'])

        taxa_evasao = (alunos_inativos / total_alunos) * 100 if total_alunos > 0 else 0

        return {
            "inativos": alunos_inativos,
            "taxa_evasao": taxa_evasao
        }