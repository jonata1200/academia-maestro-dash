import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Caminho para o banco de dados SQLite
DATABASE_PATH = os.getenv("DATABASE_PATH", "db/maestro.db")

# Outras configurações podem ser adicionadas aqui
# Ex: diretório base para arquivos de dados CSV
DATA_BASE_PATH = os.getenv("DATA_PATH", "data")

# Preço padrão para uma aula individual
PRECO_AULA_INDIVIDUAL = float(os.getenv("PRECO_AULA_INDIVIDUAL", "250.00"))

# Instrumentos suportados (pode ser carregado do DB depois)
INSTRUMENTS = ["Violão", "Teclado", "Guitarra", "Bateria", "Violino"]

# Status de aulas
AULA_STATUS = ["Agendada", "Concluída", "Cancelada"]