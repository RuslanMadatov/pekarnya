from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.views.decorators.http import require_POST

from cart.models import Cart
from cart.utils import get_user_carts
from shop.models import Product

@require_POST
def cart_add(request):

    product_id = request.POST.get("product_id")

    product = Product.objects.get(id=product_id)

    
    # if request.user.is_authenticated:
    #     carts = Cart.objects.filter(user=request.user, product=product)

    #     if carts.exists():
    #         cart = carts.first()
    #         if cart:
    #             cart.quantity += 1
    #             cart.save()
    #     else:
    #         Cart.objects.create(user=request.user, product=product, quantity=1)

    # else:
    carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
    
    if carts.exists():
      cart = carts.first()
      #  что бы не добавлять в корзину уже существующий товар
      if cart:
        # cart.quantity += 1
        # cart.save()
          # messages.warning(request,'Этот продукт уже есть в корзине')
          pass
       
    else:
        session_key = Session.objects.get(session_key=request.session.session_key)
        Cart.objects.create(session_key=session_key, product=product, quantity=1)
        
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string("cart/include/cart_buttons.html", {"carts": user_cart}, request=request)

    response_data = {
        # "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }
    
    return JsonResponse(response_data)
            
@require_POST
def cart_change(request):
    cart_id = request.POST.get("cart_id")
    
    quantity = request.POST.get("quantity")
    # if quantity == 6:
    #     messages.warning(request, "Больше 20шт одного товара нельзя")
   
    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    
    cart = get_user_carts(request)
    cart_input_html = render_to_string("cart/include/input.html", {"carts": cart}, request)
    response_data = {   
       'cart_input_html':cart_input_html,
       }    
    
    return JsonResponse(response_data)


@require_POST
def cart_remove(request):
    
    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "cart/include/cart_buttons.html", {"carts": user_cart}, request=request)
    
    cart_input_html = render_to_string("cart/include/input.html", {"carts": user_cart}, request=request)

    response_data = {
        # "message": "Товар удален",
        "cart_items_html": cart_items_html,
        'cart_input_html':cart_input_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)


def cart_detail(request):
   
    return render(request, 'cart/cart_detail.html', {'titl':'Корзина'})