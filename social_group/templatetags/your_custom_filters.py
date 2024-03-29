from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(bound_field: BoundField, css_class: str):
    if hasattr(bound_field, 'field') and hasattr(bound_field.field.widget, 'attrs'):
        attrs = bound_field.field.widget.attrs
        existing_classes = attrs.get('class', '')
        attrs['class'] = f'{existing_classes} {css_class}'.strip()
    return bound_field