from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment_process/', views.payment_process, name='payment_process'),
    path('post_payment/', views.post_payment, name='post_payment'),

]
