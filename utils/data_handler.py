import pandas as pd
import os
from config.settings import (
    DATA_XLSX_PATH, SHEET_ALUNOS, SHEET_PROFESSORES, SHEET_INSTRUMENTOS,
    SHEET_AULAS_OFERTADAS, SHEET_MATRICULAS, SHEET_AGENDA, SHEET_PAGAMENTOS
)

class DataHandler:
    def __init__(self):
        self.file_path = DATA_XLSX_PATH
        self.sheet_names = {
            'alunos': SHEET_ALUNOS,
            'professores': SHEET_PROFESSORES,
            'instrumentos': SHEET_INSTRUMENTOS,
            'aulas_ofertadas': SHEET_AULAS_OFERTADAS,
            'matriculas': SHEET_MATRICULAS,
            'agenda_aulas': SHEET_AGENDA,
            'pagamentos': SHEET_PAGAMENTOS,
        }
        self.dataframes = self._load_all_sheets()
        print(f"Gerenciador de dados Excel inicializado para o arquivo: {self.file_path}")

    def _load_all_sheets(self):
        """Carrega todas as abas do arquivo Excel para um dicionário de DataFrames."""
        if not os.path.exists(self.file_path):
            print("Arquivo Excel não encontrado. Criando um novo com abas vazias.")
            self.initialize_excel_file()
            return {name: pd.DataFrame() for name in self.sheet_names.values()}

        try:
            # Carrega todas as abas de uma vez
            return pd.read_excel(self.file_path, sheet_name=None)
        except Exception as e:
            print(f"❌ Erro ao ler o arquivo Excel: {e}")
            return {name: pd.DataFrame() for name in self.sheet_names.values()}

    def _save_all_sheets(self):
        """Salva todos os DataFrames em memória de volta para o arquivo Excel."""
        try:
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                for sheet_name, df in self.dataframes.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            print("✅ Dados salvos no arquivo Excel com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao salvar o arquivo Excel: {e}")

    def initialize_excel_file(self):
        """Cria um arquivo Excel vazio com todas as abas necessárias se ele não existir."""
        if not os.path.exists(self.file_path):
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                for sheet_name in self.sheet_names.values():
                    # Cria uma aba vazia para cada nome de sheet
                    pd.DataFrame().to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Arquivo '{self.file_path}' criado com as abas necessárias.")

    def get_data(self, table_name):
        """Retorna uma cópia do DataFrame para uma 'tabela' (aba)."""
        sheet_name = self.sheet_names.get(table_name)
        if sheet_name and sheet_name in self.dataframes:
            return self.dataframes[sheet_name].copy()
        print(f"Aviso: A aba '{sheet_name}' não foi encontrada.")
        return pd.DataFrame()

    def insert_data(self, table_name, data_df):
        """Insere novas linhas em uma 'tabela' (aba) e salva o arquivo."""
        sheet_name = self.sheet_names.get(table_name)
        if sheet_name in self.dataframes:
            # Concatena o dataframe existente com o novo
            self.dataframes[sheet_name] = pd.concat([self.dataframes[sheet_name], data_df], ignore_index=True)
            self._save_all_sheets()
        else:
            print(f"❌ Erro: A aba '{sheet_name}' não existe para inserção.")