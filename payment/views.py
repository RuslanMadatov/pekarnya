import uuid
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



from yookassa import Configuration, Payment
from orders.models import Order, OrderItem, PostCode
from cart.models import Cart
from shop.models import Product
# from payment.tasks import message_email_created
from payment.utils import random_alphanumeric_string, message_email_post_payment, admin_email_product_quantity

# from orders.tasks import order_created

# создать экземпляр юкасса
Configuration.account_id = settings.YOCASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOCASSA_SECRET_KEY


# посылает платеж юкассе,
# !!!! убрать тест в реале
@csrf_exempt
def payment_process(order_id, cart_prize):
    idempotence_key = str(uuid.uuid4())
    data = {
        "amount": {
            "value": str(cart_prize),
            "currency": "RUB"
        },

        "confirmation": {
            "type": "redirect",
            "return_url": "https://example.ru"
        },
        "capture": True,
        "test": True,
        "description": f'Заказ № {str(order_id)}',
        "metadata": {"order_id": str(order_id)}

    }

    payment = Payment.create(data, idempotence_key)
    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url


# ответ на запрос юкасса
@csrf_exempt
def post_payment(request):
    # из ответа юкассы нахожу id платежа и заказа
    data = json.loads(request.body)
    
    payment_id = data['object']["id"]
   
    payment_order_id = int(data['object']["metadata"]["order_id"])
    
    # далее добавляю в модель Order оставшиеся данные 
    order = Order.objects.get(id=payment_order_id)
    order.paid = True
    order.y_cassa_id = payment_id
    order.save()
    
    # дальнейший код не протестирован!!!!!!
    cart_items  = Cart.objects.filter(session_key = request.session.session_key)

    for cart_item in cart_items:
        product=cart_item.product
        name=cart_item.product.name
        price=cart_item.product.sell_price()
        quantity=cart_item.quantity

        OrderItem.objects.create(order=order,product=product, name=name, price=price, quantity=quantity,)
        product.quantity -= quantity
        product.save()
    
    cart_items.delete()
    order_code = random_alphanumeric_string()
    # print(order_code)
    PostCode.objects.create(order=order, order_code=order_code)


    message_email_post_payment(order_id=payment_order_id, order_code=order_code)
    admin_email_product_quantity()
    # message_email_created.delay(payment_order_id)
    # order_created.delay(payment_order_id)
    return HttpResponse(status=200)
