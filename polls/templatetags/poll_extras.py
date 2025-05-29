from django import template


register = template.Library()


@register.filter('three_digits_currency')
def three_digits_currency(value):
    return ' {: ,}'.format(value)
