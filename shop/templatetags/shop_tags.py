from django import template
from django.utils.http import urlencode
from django.core.cache import cache

from shop.models import Category



# Чтобы создавать автоматически меню
register = template.Library()
@register.simple_tag()
def tag_categories():
    category_all = cache.get('category_all')
    if category_all is None:
        category_all = Category.objects.all()
        cache.set('category_all', category_all, timeout=300)

    return category_all


# Для пагинации
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
   
    query.update(kwargs)
    return urlencode(query)