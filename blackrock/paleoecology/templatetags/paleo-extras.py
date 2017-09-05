from django import template
register = template.Library()


@register.filter
def hash(h, key):
    try:
        return h[key]
    except KeyError:
        pass


@register.filter
def soiltype(depth):
    if depth < 787:
        return "mud"
    if depth < 835:
        return "mixed"
    return "clay"


@register.filter
def contains(list, item):
    return item in list
