# analysis/financeiro_analysis.py

import pandas as pd

class FinanceiroAnalysis:
    def __init__(self, data_handler):
        """
        Inicializa a classe de análise financeira, recebendo o DataHandler.
        """
        self.handler = data_handler
        print("Analisador Financeiro (Modo Pandas) inicializado.")

    def get_faturamento_total_por_mes(self, ano):
        """
        Calcula o faturamento total por mês (considerando pagamentos concluídos).
        Lógica SQL: SELECT MONTH(data_pagamento), SUM(valor_pago) FROM pagamentos WHERE YEAR(...) AND status = 'Pago' GROUP BY MONTH(...).
        """
        df_pagamentos = self.handler.get_data('pagamentos')
        if df_pagamentos.empty:
            return pd.DataFrame(columns=['mes', 'faturamento_mensal'])

        df_pagamentos['data_pagamento'] = pd.to_datetime(df_pagamentos['data_pagamento'])

        # 1. Filtra por ano e status 'Pago'
        filtro = (df_pagamentos['data_pagamento'].dt.year == int(ano)) & (df_pagamentos['status'] == 'Pago')
        df_filtrado = df_pagamentos[filtro].copy()

        if df_filtrado.empty:
            return pd.DataFrame(columns=['mes', 'faturamento_mensal'])

        # 2. Cria uma coluna 'mes' para o agrupamento
        df_filtrado['mes'] = df_filtrado['data_pagamento'].dt.strftime('%Y-%m')
        
        # 3. Agrupa por mês e soma o valor pago
        resultado = df_filtrado.groupby('mes')['valor_pago'].sum().reset_index(name='faturamento_mensal')
        
        return resultado.sort_values('mes')

    def get_faturamento_por_instrumento(self, ano):
        """
        Calcula o faturamento gerado por cada tipo de instrumento (aula).
        """
        df_pagamentos = self.handler.get_data('pagamentos')
        df_agenda = self.handler.get_data('agenda_aulas')
        df_instrumentos = self.handler.get_data('instrumentos')

        if df_pagamentos.empty or df_agenda.empty or df_instrumentos.empty:
            return pd.DataFrame()

        df_pagamentos['data_pagamento'] = pd.to_datetime(df_pagamentos['data_pagamento'])
        
        # 1. Filtra pagamentos por ano e status
        filtro = (df_pagamentos['data_pagamento'].dt.year == int(ano)) & (df_pagamentos['status'] == 'Pago')
        pagamentos_validos = df_pagamentos[filtro]

        # 2. Junta pagamentos com agenda e depois com instrumentos
        merge1 = pd.merge(pagamentos_validos, df_agenda, left_on='referencia_aula_id', right_on='id')
        merge2 = pd.merge(merge1, df_instrumentos, left_on='instrumento_id', right_on='id')
        
        # 3. Agrupa por nome do instrumento e soma os valores
        resultado = merge2.groupby('nome_instrumento')['valor_pago'].sum().reset_index(name='faturamento_instrumento')
        
        return resultado.sort_values('faturamento_instrumento', ascending=False)

    def get_top_alunos_faturamento(self, top_n=5, ano='2024'):
        """
        Retorna os alunos que mais contribuíram para o faturamento.
        """
        df_pagamentos = self.handler.get_data('pagamentos')
        df_alunos = self.handler.get_data('alunos')

        if df_pagamentos.empty or df_alunos.empty:
            return pd.DataFrame()

        df_pagamentos['data_pagamento'] = pd.to_datetime(df_pagamentos['data_pagamento'])
        
        # 1. Filtra pagamentos
        filtro = (df_pagamentos['data_pagamento'].dt.year == int(ano)) & (df_pagamentos['status'] == 'Pago')
        pagamentos_validos = df_pagamentos[filtro]

        # 2. Junta com alunos
        df_merged = pd.merge(pagamentos_validos, df_alunos, left_on='aluno_id', right_on='id')
        
        # 3. Agrupa por nome do aluno e soma os gastos
        resultado = df_merged.groupby('nome')['valor_pago'].sum().reset_index(name='total_gasto')
        
        # 4. Ordena e pega o 'top N'
        resultado = resultado.sort_values('total_gasto', ascending=False)
        return resultado.head(top_n)

    def get_faturamento_por_professor(self, ano='2024'):
        """
        Calcula o faturamento (receita bruta) gerado por cada professor.
        """
        df_pagamentos = self.handler.get_data('pagamentos')
        df_agenda = self.handler.get_data('agenda_aulas')
        df_professores = self.handler.get_data('professores')
        
        if df_pagamentos.empty or df_agenda.empty or df_professores.empty:
            return pd.DataFrame()
        
        df_pagamentos['data_pagamento'] = pd.to_datetime(df_pagamentos['data_pagamento'])
        
        # 1. Filtra pagamentos
        filtro = (df_pagamentos['data_pagamento'].dt.year == int(ano)) & (df_pagamentos['status'] == 'Pago')
        pagamentos_validos = df_pagamentos[filtro]

        # 2. Junta pagamentos -> agenda -> professores
        merge1 = pd.merge(pagamentos_validos, df_agenda, left_on='referencia_aula_id', right_on='id')
        merge2 = pd.merge(merge1, df_professores, left_on='professor_id', right_on='id')
        
        # 3. Agrupa por nome do professor e soma os valores
        resultado = merge2.groupby('nome')['valor_pago'].sum().reset_index(name='faturamento_professor')
        resultado = resultado.rename(columns={'nome': 'nome_professor'})
        
        return resultado.sort_values('faturamento_professor', ascending=False)