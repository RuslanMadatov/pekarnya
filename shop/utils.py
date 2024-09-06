from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from pshop.settings import ADMINS, EMAIL_HOST_USER


# письмо админу при получении отзыва
def feedback_mail_admin():
    template_html = render_to_string('shop/otcher/feedback_mail_admin.html')
    subject = f'Отзыв'
    msg = EmailMultiAlternatives(subject, template_html, EMAIL_HOST_USER,
                                 [a[1] for a in ADMINS])
    msg.content_subtype = "html"
    msg.send()