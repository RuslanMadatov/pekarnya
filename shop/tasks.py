"""
Отклчил celery. Не хватало оперативной памяти на реальном сервере или произошла утечка памяти
"""


# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from celery import shared_task
# from pshop.settings import ADMINS, EMAIL_HOST_USER


# @shared_task
# def feedback_mail_admin():
#     template_html = render_to_string('shop/otcher/feedback_mail_admin.html')
#     subject = f'Отзыв'
#     msg = EmailMultiAlternatives(subject, template_html, EMAIL_HOST_USER,
#                                  [a[1] for a in ADMINS])
#     msg.content_subtype = "html"
#     msg.send()
