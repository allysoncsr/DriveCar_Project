from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    """Adiciona classes CSS a um campo de formulário no template.

    Uso: {{ form.field|add_class:'input input-sm' }}
    """
    try:
        existing = field.field.widget.attrs.get('class', '')
        classes = (existing + ' ' + css_class).strip()
        return field.as_widget(attrs={'class': classes})
    except Exception:
        return field

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Obtém um item de um dicionário no template.
    
    Uso: {{ dict|get_item:key }}
    """
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return None
