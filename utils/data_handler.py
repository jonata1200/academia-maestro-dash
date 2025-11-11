import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine, text
from config.settings import DATABASE_PATH, DATA_BASE_PATH
import datetime

class DataHandler:
    def __init__(self, db_path=DATABASE_PATH, data_base_path=DATA_BASE_PATH):
        self.db_path = db_path
        self.data_base_path = data_base_path
        self.engine = create_engine(f'sqlite:///{self.db_path}')

    def _get_db_connection(self):
        """Retorna uma conexão bruta com o SQLite."""
        return sqlite3.connect(self.db_path)

    def fetch_data_from_db(self, table_name, columns='*', condition=None):
        """
        Busca dados de uma tabela do banco de dados.
        :param table_name: Nome da tabela.
        :param columns: Colunas a serem selecionadas (string ou lista). Default: '*'.
        :param condition: Condição WHERE em SQL (ex: "status = 'Ativo'"). Default: None.
        :return: DataFrame do Pandas com os dados.
        """
        cols_str = ', '.join(columns) if isinstance(columns, list) else columns
        query = f"SELECT {cols_str} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        print(f"Executando query no DB: {query}")
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql(text(query), connection)
            return df
        except Exception as e:
            print(f"Erro ao buscar dados da tabela '{table_name}': {e}")
            return pd.DataFrame()

    def insert_data_into_db(self, table_name, data_df):
        """
        Insere um DataFrame no banco de dados.
        :param table_name: Nome da tabela.
        :param data_df: DataFrame do Pandas com os dados a serem inseridos.
        """
        try:
            data_df.to_sql(table_name, self.engine, if_exists='append', index=False)
            print(f"✅ {len(data_df)} registros inseridos na tabela '{table_name}'.")
        except Exception as e:
            print(f"❌ Erro ao inserir dados na tabela '{table_name}': {e}")

    def update_data_in_db(self, table_name, data_dict, condition):
        """
        Atualiza registros em uma tabela.
        :param table_name: Nome da tabela.
        :param data_dict: Dicionário com colunas e novos valores para atualizar.
        :param condition: Condição WHERE em SQL para os registros a serem atualizados.
        """
        set_clause = ", ".join([f"{col} = ?" for col in data_dict.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        values = list(data_dict.values())
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
            print(f"✅ Registros atualizados na tabela '{table_name}' com a condição '{condition}'.")
        except Exception as e:
            print(f"❌ Erro ao atualizar dados na tabela '{table_name}': {e}")

    def delete_data_from_db(self, table_name, condition):
        """
        Deleta registros de uma tabela.
        :param table_name: Nome da tabela.
        :param condition: Condição WHERE em SQL para os registros a serem deletados.
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
            print(f"✅ Registros deletados da tabela '{table_name}' com a condição '{condition}'.")
        except Exception as e:
            print(f"❌ Erro ao deletar dados da tabela '{table_name}': {e}")

    def read_csv_data(self, filename, year='2024'):
        """
        Lê um arquivo CSV de um ano específico e retorna um DataFrame.
        :param filename: Nome do arquivo CSV (ex: "alunos.csv").
        :param year: Ano da pasta de dados.
        :return: DataFrame do Pandas.
        """
        file_path = os.path.join(self.data_base_path, str(year), filename)
        if not os.path.exists(file_path):
            print(f"❌ Erro: Arquivo CSV não encontrado: {file_path}")
            return pd.DataFrame()
        try:
            df = pd.read_csv(file_path)
            print(f"✅ CSV '{filename}' lido com sucesso ({len(df)} registros).")
            return df
        except Exception as e:
            print(f"❌ Erro ao ler CSV '{filename}': {e}")
            return pd.DataFrame()

    def write_csv_data(self, df, filename, year='2024', mode='w', header=True):
        """
        Escreve um DataFrame para um arquivo CSV.
        :param df: DataFrame do Pandas a ser escrito.
        :param filename: Nome do arquivo CSV.
        :param year: Ano da pasta de dados.
        :param mode: Modo de escrita ('w' para sobrescrever, 'a' para anexar).
        :param header: Incluir cabeçalho (True/False).
        """
        output_dir = os.path.join(self.data_base_path, str(year))
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        try:
            df.to_csv(file_path, mode=mode, header=header, index=False)
            print(f"✅ DataFrame escrito para '{file_path}' com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao escrever CSV '{filename}': {e}")

# Exemplo de uso:
if __name__ == "__main__":
    # Importante: O banco de dados e as tabelas devem existir para testar
    # Execute etl/migrate_csv_to_sqlite.py primeiro!
    print("Testando DataHandler...")
    handler = DataHandler()

    # Testar fetch_data_from_db
    print("\n--- Buscando dados de instrumentos ---")
    instrumentos_df = handler.fetch_data_from_db('instrumentos')
    print(instrumentos_df)

    print("\n--- Buscando alunos ativos ---")
    alunos_ativos_df = handler.fetch_data_from_db('alunos', condition="status = 'Ativo'")
    print(alunos_ativos_df)

    # Testar insert_data_into_db (cria um aluno temporário)
    print("\n--- Inserindo novo aluno ---")
    new_student_data = {
        'nome': ['Testador da Silva'],
        'data_nascimento': ['2000-01-01'],
        'genero': ['Masculino'],
        'email': ['testador.silva@email.com'],
        'telefone': ['999998888'],
        'data_cadastro': [datetime.datetime.now()],
        'status': ['Ativo']
    }
    new_student_df = pd.DataFrame(new_student_data)
    handler.insert_data_into_db('alunos', new_student_df)

    # Verificar se o aluno foi inserido
    print("\n--- Verificando novo aluno inserido ---")
    all_alunos_df = handler.fetch_data_from_db('alunos')
    print(all_alunos_df.tail()) # Mostrar os últimos para ver o novo

    # Testar update_data_in_db
    print("\n--- Atualizando status do aluno Testador da Silva ---")
    update_data = {'status': 'Inativo', 'telefone': '999997777'}
    handler.update_data_in_db('alunos', update_data, "email = 'testador.silva@email.com'")

    # Verificar atualização
    print("\n--- Verificando aluno Testador da Silva após atualização ---")
    updated_aluno = handler.fetch_data_from_db('alunos', condition="email = 'testador.silva@email.com'")
    print(updated_aluno)

    # Testar delete_data_from_db
    print("\n--- Deletando aluno Testador da Silva ---")
    handler.delete_data_from_db('alunos', "email = 'testador.silva@email.com'")

    # Verificar deleção
    print("\n--- Verificando se aluno Testador da Silva foi deletado ---")
    deleted_aluno_check = handler.fetch_data_from_db('alunos', condition="email = 'testador.silva@email.com'")
    print(deleted_aluno_check) # Deve ser um DataFrame vazio

    # Testar read_csv_data (assumindo que você tem um alunos.csv em data/2024/)
    print("\n--- Lendo dados de alunos.csv ---")
    alunos_csv_df = handler.read_csv_data('alunos.csv', year='2024')
    print(alunos_csv_df.head())

    # Testar write_csv_data (escrevendo um CSV temporário)
    print("\n--- Escrevendo um CSV temporário ---")
    temp_df = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
    handler.write_csv_data(temp_df, 'temp_test.csv', year='2024')

    # Deletar o CSV temporário
    temp_file_path = os.path.join(DATA_BASE_PATH, '2024', 'temp_test.csv')
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(f"Arquivo temporário '{temp_file_path}' removido.")