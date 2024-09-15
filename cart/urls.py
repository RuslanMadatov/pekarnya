from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailViev.as_view(), name='cart_detail'),
    path('add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart_change/', views.CartChangeView.as_view(), name='cart_change'),
    path('remove/', views.CartRemoveView.as_view(), name='cart_remove'),
]
