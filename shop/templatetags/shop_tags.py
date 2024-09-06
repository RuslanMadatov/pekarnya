from django import template
from django.utils.http import urlencode

from shop.models import Category


# Чтобы создавать автоматически меню
register = template.Library()
@register.simple_tag()
def tag_categories():
    return Category.objects.all()


# Для пагинации
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
   
    query.update(kwargs)
    return urlencode(query)