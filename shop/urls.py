from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('contacts/', views.ContaktView.as_view(), name='contacts'),
    path('feedback/', views.fedbackview, name='feedback'),
    path('search/<slug:category_slug>/', views.product_list, name='search'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    
    path('<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
    

]
