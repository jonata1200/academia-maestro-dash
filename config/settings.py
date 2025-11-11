import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Caminho para o "banco de dados" em formato Excel
# Teremos um único arquivo com várias abas (sheets)
DATA_XLSX_PATH = os.getenv("DATA_XLSX_PATH", "data/academia_maestro_dados.xlsx")

# Nomes das abas que usaremos no arquivo Excel
# Usar constantes evita erros de digitação no resto do código
SHEET_ALUNOS = "alunos"
SHEET_PROFESSORES = "professores"
SHEET_INSTRUMENTOS = "instrumentos"
SHEET_AULAS_OFERTADAS = "aulas_ofertadas"
SHEET_MATRICULAS = "matriculas"
SHEET_AGENDA = "agenda_aulas"
SHEET_PAGAMENTOS = "pagamentos"

# Outras configurações podem ser mantidas
PRECO_AULA_INDIVIDUAL = float(os.getenv("PRECO_AULA_INDIVIDUAL", "250.00"))