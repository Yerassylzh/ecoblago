from django import template

register = template.Library()

@register.filter
def thousand_separator(value):
    try:
        return f"{int(value):,}".replace(",", " ")
    except (ValueError, TypeError):
        return value

@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value

@register.filter
def get_item_at(lst, index):
    try:
        return lst[index]
    except (IndexError, TypeError):
        return None

@register.filter
def multiply(value, arg):
    try:
        return str(float(value) * int(arg))
    except (TypeError, ValueError):
        return None

@register.filter
def to_float(value, precision=2):
    try:
        return str(float(f"{value: .{precision}f}"))
    except (ValueError, TypeError):
        return value