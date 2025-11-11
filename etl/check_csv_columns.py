import pandas as pd
import os
from config.settings import DATA_BASE_PATH

# Definir as colunas esperadas para cada arquivo CSV
EXPECTED_COLUMNS = {
    'alunos.csv': ['id', 'nome', 'data_nascimento', 'genero', 'email', 'telefone', 'data_cadastro', 'status'],
    'professores.csv': ['id', 'nome', 'email', 'telefone', 'data_contratacao', 'especializacao', 'status'],
    'instrumentos.csv': ['id', 'nome_instrumento'],
    'aulas_ofertadas.csv': ['id', 'nome_aula', 'instrumento_id'],
    'matriculas.csv': ['id', 'aluno_id', 'aula_ofertada_id', 'data_matricula', 'data_fim_matricula', 'status'],
    'agenda_aulas.csv': ['id', 'aluno_id', 'professor_id', 'instrumento_id', 'data_aula', 'hora_inicio', 'hora_fim', 'valor_aula', 'status', 'observacoes'],
    'pagamentos.csv': ['id', 'aluno_id', 'data_pagamento', 'valor_pago', 'metodo_pagamento', 'referencia_aula_id', 'status', 'observacoes']
    # Adicione outros CSVs conforme a necessidade
}

def check_csv_columns(file_path, expected_cols):
    """
    Verifica se um arquivo CSV possui todas as colunas esperadas.
    Retorna True se sim, False caso contrário, e uma lista de colunas ausentes.
    """
    if not os.path.exists(file_path):
        print(f"Aviso: Arquivo CSV não encontrado: {file_path}")
        return False, ["Arquivo não encontrado"]

    try:
        df = pd.read_csv(file_path, nrows=0) # Lê apenas o cabeçalho
        actual_cols = set(df.columns.tolist())
        expected_cols_set = set(expected_cols)

        missing_cols = list(expected_cols_set - actual_cols)
        extra_cols = list(actual_cols - expected_cols_set)

        if not missing_cols:
            print(f"✅ {os.path.basename(file_path)}: Todas as colunas esperadas estão presentes.")
            if extra_cols:
                print(f"   (Colunas extras encontradas: {', '.join(extra_cols)})")
            return True, []
        else:
            print(f"❌ {os.path.basename(file_path)}: Colunas ausentes: {', '.join(missing_cols)}")
            if extra_cols:
                print(f"   (Colunas extras encontradas: {', '.join(extra_cols)})")
            return False, missing_cols
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return False, [str(e)]

def run_all_csv_checks(base_data_path=DATA_BASE_PATH, year='2024'):
    """
    Executa a verificação de colunas para todos os CSVs esperados em um determinado ano.
    """
    data_year_path = os.path.join(base_data_path, str(year))
    print(f"Verificando arquivos CSV na pasta: {data_year_path}")
    all_ok = True
    for filename, expected_cols in EXPECTED_COLUMNS.items():
        file_path = os.path.join(data_year_path, filename)
        is_ok, missing = check_csv_columns(file_path, expected_cols)
        if not is_ok and "Arquivo não encontrado" not in missing:
            all_ok = False
    return all_ok

if __name__ == "__main__":
    print("Iniciando verificação de colunas CSV...")
    # Crie a pasta data/2024 e alguns CSVs vazios com apenas o cabeçalho
    # para testar este script, ou apenas execute junto com o migrate_csv_to_sqlite.py
    # que irá criar um banco vazio.
    # Exemplo:
    # os.makedirs(os.path.join(DATA_BASE_PATH, '2024'), exist_ok=True)
    # for filename, cols in EXPECTED_COLUMNS.items():
    #     with open(os.path.join(DATA_BASE_PATH, '2024', filename), 'w') as f:
    #         f.write(','.join(cols) + '\n')
    #
    if run_all_csv_checks(year='2024'):
        print("\nTodas as verificações de colunas CSV concluídas com sucesso!")
    else:
        print("\nAlgumas verificações de colunas CSV falharam. Por favor, revise os arquivos.")