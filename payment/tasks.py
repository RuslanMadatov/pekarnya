"""
Отклчил celery. Не хватало оперативной памяти на реальном сервере или произошла утечка памяти
"""

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from celery import shared_task
# from orders.models import Order


# @shared_task
# def message_email_created(order_id):
#     order = Order.objects.get(id=order_id)
#     user_name = order.first_name
#     template_html = render_to_string('payment/email.html', {'user_name': user_name, 'order_id': order_id})
#     subject = f'Номер заказа {order.id}'
#     msg = EmailMultiAlternatives(subject, template_html, 'ruslan_mio666_61289@mail.ru', [order.email])
#     msg.content_subtype = "html"
#     return msg.send()
