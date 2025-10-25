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
