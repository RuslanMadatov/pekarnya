# from celery import shared_task
# from django.core.management import call_command


# @shared_task
# def order_created(order_id):
#     """
#     Задание по отправке уведомления по электронной почте
#     при успешном создании заказа.
#     """
#     order = Order.objects.get(id=order_id)
#     subject = f'Номер заказа. {order.id}'
#     message = f'Уважаемый {order.first_name},\n\n' \
#               f'Ваш заказ оплачен \n' \
#               f'Ваш номер заказа {order.id}. Позже мы вышлем Вам чек.'
#     mail_sent = send_mail(subject, message, 'ruslan_mio666_61289@mail.ru', [order.email])
#     return mail_sent


# @shared_task(bind=True)
# def hello_world(self):
#     print('Проверка периодических событий')


# @shared_task(bind=True)
# def clean_db(self):
#     call_command('clearsessions')
