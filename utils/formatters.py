import pandas as pd
from datetime import datetime

def format_currency(value, currency_symbol="R$"):
    """
    Formata um valor numérico para o formato de moeda brasileira.
    Ex: 1234.50 -> R$ 1.234,50
    """
    try:
        if pd.isna(value):
            return f"{currency_symbol} 0,00"
        return f"{currency_symbol} {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return f"{currency_symbol} 0,00"

def format_date(date_obj, fmt="%d/%m/%Y"):
    """
    Formata um objeto datetime ou string de data para o formato especificado.
    """
    if pd.isna(date_obj):
        return ""
    try:
        if isinstance(date_obj, str):
            # Tenta converter string para datetime
            date_obj = pd.to_datetime(date_obj)
        return date_obj.strftime(fmt)
    except (ValueError, TypeError):
        return str(date_obj) # Retorna a string original ou representação se falhar

def format_time(time_obj, fmt="%H:%M"):
    """
    Formata um objeto time ou string de hora para o formato especificado.
    """
    if pd.isna(time_obj):
        return ""
    try:
        if isinstance(time_obj, str):
            # Se for string, tenta criar um objeto datetime temporário
            # para extrair o tempo, ou assume que já está no formato correto.
            # Idealmente, você armazenaria como TIME ou DATETIME no DB.
            return datetime.strptime(time_obj, fmt).strftime(fmt)
        return time_obj.strftime(fmt)
    except (ValueError, TypeError):
        return str(time_obj)

def format_percentage(value, decimals=2):
    """
    Formata um valor numérico como porcentagem.
    Ex: 0.75 -> 75.00%
    """
    try:
        if pd.isna(value):
            return "0.00%"
        return f"{value:.{decimals}f}%"
    except (ValueError, TypeError):
        return "0.00%"

def clean_phone_number(phone_number):
    """
    Limpa e padroniza números de telefone (remove não-dígitos).
    """
    if pd.isna(phone_number) or not isinstance(phone_number, str):
        return ""
    return ''.join(filter(str.isdigit, phone_number))

def display_status(status_text):
    """
    Pode ser usado para mapear status para uma exibição mais amigável ou com ícones.
    """
    status_map = {
        'Ativo': '🟢 Ativo',
        'Inativo': '🔴 Inativo',
        'Suspensa': '🟡 Suspensa',
        'Agendada': '🗓️ Agendada',
        'Concluída': '✅ Concluída',
        'Cancelada': '❌ Cancelada',
        'Pendente': '⏳ Pendente',
        'Pago': '💰 Pago',
        # Adicione outros status conforme necessário
    }
    return status_map.get(status_text, status_text)

# Exemplo de uso:
if __name__ == "__main__":
    print("Testando Formatters...")

    # Teste de format_currency
    print(f"Moeda (1234.5): {format_currency(1234.5)}")
    print(f"Moeda (1234.567): {format_currency(1234.567)}")
    print(f"Moeda (100): {format_currency(100)}")
    print(f"Moeda (None): {format_currency(None)}")
    print(f"Moeda (0): {format_currency(0)}")

    # Teste de format_date
    hoje = datetime.now()
    data_str = "2023-01-15"
    print(f"Data (datetime): {format_date(hoje)}")
    print(f"Data (string YYYY-MM-DD): {format_date(data_str)}")
    print(f"Data (None): {format_date(None)}")
    print(f"Data (formato customizado): {format_date(hoje, '%Y-%m-%d %H:%M')}")

    # Teste de format_time
    hora_agora = datetime.now().time()
    hora_str = "14:30"
    print(f"Hora (time obj): {format_time(hora_agora)}")
    print(f"Hora (string HH:MM): {format_time(hora_str)}")
    print(f"Hora (None): {format_time(None)}")

    # Teste de format_percentage
    print(f"Porcentagem (0.75): {format_percentage(0.75)}")
    print(f"Porcentagem (0.12345): {format_percentage(0.12345, decimals=1)}")
    print(f"Porcentagem (None): {format_percentage(None)}")

    # Teste de clean_phone_number
    print(f"Telefone Limpo ('(11) 98765-4321'): {clean_phone_number('(11) 98765-4321')}")
    print(f"Telefone Limpo ('+55 11 987654321'): {clean_phone_number('+55 11 987654321')}")
    print(f"Telefone Limpo (None): {clean_phone_number(None)}")

    # Teste de display_status
    print(f"Status 'Ativo': {display_status('Ativo')}")
    print(f"Status 'Agendada': {display_status('Agendada')}")
    print(f"Status 'Concluída': {display_status('Concluída')}")
    print(f"Status 'Desconhecido': {display_status('Desconhecido')}")