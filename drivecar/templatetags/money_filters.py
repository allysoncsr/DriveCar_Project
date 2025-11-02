from django import template
from decimal import Decimal
import locale

register = template.Library()

@register.filter
def money_br(value):
    """
    Formata um valor numérico como moeda brasileira
    Exemplo: 1234.56 -> R$ 1.234,56
    """
    if value is None:
        return "R$ 0,00"
    
    try:
        # Converte para Decimal se não for
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        
        # Formatar como moeda brasileira
        value_str = f"{value:.2f}"
        
        # Separar parte inteira e decimal
        parts = value_str.split('.')
        integer_part = parts[0]
        decimal_part = parts[1]
        
        # Adicionar pontos nos milhares
        if len(integer_part) > 3:
            # Reverter string, adicionar pontos a cada 3 dígitos, reverter novamente
            reversed_int = integer_part[::-1]
            formatted_int = ''
            for i, digit in enumerate(reversed_int):
                if i > 0 and i % 3 == 0:
                    formatted_int += '.'
                formatted_int += digit
            integer_part = formatted_int[::-1]
        
        return f"R$ {integer_part},{decimal_part}"
        
    except (ValueError, TypeError, AttributeError):
        return "R$ 0,00"


@register.filter
def get_item(dictionary, key):
    """
    Filtro para acessar itens de dicionário usando chaves dinâmicas
    Uso: {{ dict|get_item:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def div(value, divisor):
    """
    Filtro para divisão
    Uso: {{ valor|div:divisor }}
    """
    try:
        if divisor and float(divisor) != 0:
            return float(value) / float(divisor)
        return 0
    except (ValueError, TypeError):
        return 0


@register.filter
def mul(value, multiplicador):
    """
    Filtro para multiplicação
    Uso: {{ valor|mul:multiplicador }}
    """
    try:
        return float(value) * float(multiplicador)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, divisor):
    """
    Filtro para divisão (alias para div)
    Uso: {{ valor|divide:divisor }}
    """
    try:
        if divisor and float(divisor) != 0:
            return float(value) / float(divisor)
        return 0
    except (ValueError, TypeError):
        return 0