import uuid
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User

from yookassa import Configuration, Payment

from orders.models import Order, OrderItem, PostCode
from cart.models import Cart

# from payment.tasks import message_email_created
from payment.utils import (
    random_alphanumeric_string,
    message_email_post_payment,
    admin_email_product_quantity,
)

# from orders.tasks import order_created

# создать экземпляр юкасса
Configuration.account_id = settings.YOCASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOCASSA_SECRET_KEY


# посылает платеж юкассе
# !!!! убрать тест в реале
@csrf_exempt
def payment_process(cart_price, session_key):
    order = Order.objects.filter(session_key=session_key, paid=False)
    order_id = order.pk
    idempotence_key = str(uuid.uuid4())
    data = {
        "amount": {"value": str(cart_price), "currency": "RUB"},
        "confirmation": {"type": "redirect", "return_url": "https://example.ru"},
        "capture": True,
        "test": True,
        "description": f"Заказ № {str(order_id)}",
        "metadata": {"order_id": str(order_id)},
    }

    payment = Payment.create(data, idempotence_key)
    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url


#  для API
@csrf_exempt
def payment_process_api(cart_price, order_id, request=None):
    idempotence_key = str(uuid.uuid4())
    data = {
        "amount": {"value": str(cart_price), "currency": "RUB"},
        "confirmation": {"type": "redirect", "return_url": "https://example.ru"},
        "capture": True,
        "test": True,
        "description": f"Заказ № {str(order_id)}",
        "metadata": {"order_id": str(order_id)},
    }

    payment = Payment.create(data, idempotence_key)
    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url


# ответ на запрос юкасса
@csrf_exempt
def post_payment(request):
    cart_items = None
    user_pk = None
    # из ответа юкассы нахожу id платежа и заказа
    data = json.loads(request.body)

    payment_id = data["object"]["id"]

    payment_order_id = int(data["object"]["metadata"]["order_id"])

    # далее добавляю в модель Order оставшиеся данные
    order = Order.objects.get(id=payment_order_id)
    order.paid = True
    order.y_cassa_id = payment_id
    order.save()
    user_order = order.user
    key_session = order.session_key
    # дальнейший код не протестирован!!!!!!
    if key_session:

        cart_items = Cart.objects.filter(session_key=key_session)
    elif user_order:
        user_pk = User.objects.get(pk=user_order)
        cart_items = Cart.objects.filter(user=user_pk)

    for cart_item in cart_items:
        product = cart_item.product
        product_discount = product.discount
        name = cart_item.product.name
        price = cart_item.product.sell_price()
        quantity = cart_item.quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            name=name,
            price=price,
            quantity=quantity,
            user=user_pk,
            discount = product_discount
        )
        product.quantity -= quantity
        product.save()

    cart_items.delete()
    order_code = random_alphanumeric_string()
    PostCode.objects.create(order=order, order_code=order_code)

    message_email_post_payment(order_id=payment_order_id, order_code=order_code)
    admin_email_product_quantity()
    # message_email_created.delay(payment_order_id)
    # order_created.delay(payment_order_id)
    return HttpResponse(status=200)
