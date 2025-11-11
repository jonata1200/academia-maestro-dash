import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from config.settings import DATABASE_PATH, DATA_BASE_PATH
from etl.check_csv_columns import EXPECTED_COLUMNS, check_csv_columns

class DatabaseMigrator:
    def __init__(self, db_path=DATABASE_PATH, data_base_path=DATA_BASE_PATH):
        self.db_path = db_path
        self.data_base_path = data_base_path
        self.db_dir = os.path.dirname(self.db_path)
        self.schema_dir = 'db/schema' # Caminho relativo da raiz do projeto
        self.engine = create_engine(f'sqlite:///{self.db_path}')

        def _execute_sql_file(self, sql_file_path):
          """Executa um arquivo SQL no banco de dados."""
          print(f"Tentando executar SQL file: {sql_file_path}")  # Depuração
          if not os.path.exists(sql_file_path):
            print(f"❌ Erro: Arquivo SQL não encontrado NO CAMINHO ESPECIFICADO: {sql_file_path}")
            raise FileNotFoundError(f"Arquivo SQL não encontrado: {sql_file_path}")

        try:
            with open(sql_file_path, 'r') as f:
                sql_script = f.read()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executescript(sql_script)
            print(f"✅ {sql_file_path} executado com sucesso.")
        except sqlite3.Error as e:
            print(f"❌ Erro ao executar SQL de {sql_file_path}: {e}")
            raise


def seed_initial_data(self):
    """Popula o banco com dados iniciais (instrumentos, aulas, preços)."""
    # Executa 002_seed_instrumentos_e_aulas.sql
    # Usamos os.path.join para garantir o separador de caminho correto para o OS
    seed_instr_aulas_sql = os.path.join(self.schema_dir, '002_seed_instrumentos_e_aulas.sql')
    self._execute_sql_file(seed_instr_aulas_sql)

    # Executa 003_seed_precos_aulas.sql
    seed_precos_sql = os.path.join(self.schema_dir, '003_seed_precos_aulas.sql')
    self._execute_sql_file(seed_precos_sql)

    def migrate_csv_to_db(self, year='2024'):
        """
        Migra dados de arquivos CSV para o banco de dados.
        Ignora tabelas que já foram populadas por seed (instrumentos, aulas_ofertadas).
        """
        print(f"\nIniciando migração de CSVs para o DB para o ano {year}...")
        data_year_path = os.path.join(self.data_base_path, str(year))

        if not os.path.exists(data_year_path):
            print(f"Aviso: Diretório de dados para {year} não encontrado: {data_year_path}. Pulando migração de CSV.")
            return

        for filename, expected_cols in EXPECTED_COLUMNS.items():
            table_name = filename.replace('.csv', '')
            file_path = os.path.join(data_year_path, filename)

            # Algumas tabelas são populadas por scripts SQL.
            # Evitamos sobrescrever ou duplicar se já houver dados mestres.
            if table_name in ['instrumentos', 'aulas_ofertadas', 'professores_instrumentos', 'configuracoes']:
                print(f"Pulando migração de CSV para '{table_name}', pois é populado por script SQL.")
                continue

            if not os.path.exists(file_path):
                print(f"Aviso: CSV '{filename}' não encontrado em {data_year_path}. Pulando.")
                continue

            # Verifica a consistência das colunas antes de migrar
            is_ok, missing_cols = check_csv_columns(file_path, expected_cols)
            if not is_ok:
                print(f"❌ Não foi possível migrar '{filename}' devido a colunas ausentes ou erro.")
                continue

            try:
                df = pd.read_csv(file_path)
                if not df.empty:
                    # Ajustes específicos de tipo de dado ou formato antes da inserção
                    # Exemplo: converter 'data_nascimento' para o formato DATE do SQLite se necessário
                    if 'data_nascimento' in df.columns:
                        df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], errors='coerce').dt.date

                    if 'data_cadastro' in df.columns:
                        df['data_cadastro'] = pd.to_datetime(df['data_cadastro'], errors='coerce')

                    if 'data_contratacao' in df.columns:
                        df['data_contratacao'] = pd.to_datetime(df['data_contratacao'], errors='coerce').dt.date

                    if 'data_aula' in df.columns:
                        df['data_aula'] = pd.to_datetime(df['data_aula'], errors='coerce').dt.date

                    if 'data_matricula' in df.columns:
                        df['data_matricula'] = pd.to_datetime(df['data_matricula'], errors='coerce')

                    if 'data_pagamento' in df.columns:
                        df['data_pagamento'] = pd.to_datetime(df['data_pagamento'], errors='coerce')

                    # Escreve o DataFrame no banco de dados
                    df.to_sql(table_name, self.engine, if_exists='append', index=False)
                    print(f"✅ CSV '{filename}' migrado para a tabela '{table_name}' com {len(df)} registros.")
                else:
                    print(f"Aviso: CSV '{filename}' está vazio. Nenhuma migração para a tabela '{table_name}'.")
            except Exception as e:
                print(f"❌ Erro ao migrar '{filename}' para a tabela '{table_name}': {e}")

    def run_full_migration(self, years=['2024']):
        """Executa o processo completo de migração: cria tabelas e migra CSVs."""
        print("Iniciando processo de migração completa do banco de dados...")
        self.create_database_and_tables()
        self.seed_initial_data()
        for year in years:
            self.migrate_csv_to_db(year)
        print("Processo de migração completa finalizado.")

if __name__ == "__main__":
    # Garante que o diretório de dados existe para o teste
    # Você pode criar CSVs de exemplo aqui para testar a migração
    # Ex:
    # os.makedirs(os.path.join(DATA_BASE_PATH, '2024'), exist_ok=True)
    # with open(os.path.join(DATA_BASE_PATH, '2024', 'alunos.csv'), 'w') as f:
    #     f.write("id,nome,email\n1,João Silva,joao.silva@email.com\n2,Maria Oliveira,maria.oliveria@email.com\n")

    migrator = DatabaseMigrator()
    migrator.run_full_migration(years=['2024']) # Pode adicionar mais anos conforme necessário

    # Opcional: Verificar se as tabelas foram criadas e populadas
    # com sqlite3.connect(DATABASE_PATH) as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #     print("\nTabelas no DB:", cursor.fetchall())
    #     cursor.execute("SELECT * FROM instrumentos;")
    #     print("Instrumentos:", cursor.fetchall())
    #     cursor.execute("SELECT * FROM configuracoes;")
    #     print("Configurações:", cursor.fetchall())