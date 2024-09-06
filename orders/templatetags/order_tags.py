from django import template
from django.contrib import messages
from cart.models import Cart

register = template.Library()

@register.simple_tag()
def quantyty_product(request):
  carts  = Cart.objects.filter(session_key = request.session.session_key)
  for cart in carts:
    product = cart.product
    quantity=cart.quantity
    name=cart.product.name

    if product.quantyty < quantity:
      messages.warning(request, f'Недостаточное количество товара "{name}" на складе\
                                                       В наличии - {product.quantyty}')
  return('')  
