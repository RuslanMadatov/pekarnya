from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('checking/', views.checking_orders, name='checking_orders'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]
