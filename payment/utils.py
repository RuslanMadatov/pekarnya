import random
import string

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pshop.settings import ADMINS, EMAIL_HOST_USER

from orders.models import Order
from shop.models import Product


# создание рандомных символов для ключа модели POSTCODE в orders
def random_alphanumeric_string(length=10):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )

# посылка письма заказчику после оплаты товара
def message_email_post_payment(order_id, order_code):
    order = Order.objects.get(id=order_id)
    user_name = order.first_name
    template_html = render_to_string('payment/email.html', {'user_name': user_name, 'order_id': order_code,})
    subject = f'Номер заказа'
    msg = EmailMultiAlternatives(subject, template_html, 'ruslan_mio666_61289@mail.ru', [order.email])
    msg.content_subtype = "html"
    msg.send()

# не реализовано в проекте
# посылка письма админу если определенного товара мало
def admin_email_product_quantity():
    products = Product.objects.filter(available=True, quantyty__lte=10)
    if products.exists():
      template_html = render_to_string('payment/admin_email_product_quantity.html', {'products':products})
      subject = f'Количество продуктов'
      msg = EmailMultiAlternatives(subject, template_html, EMAIL_HOST_USER,
                                  [a[1] for a in ADMINS])
      msg.content_subtype = "html"
      msg.send()
