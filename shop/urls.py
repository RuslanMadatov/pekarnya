from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('contacts/', views.ContaktView.as_view(), name='contacts'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('search/<slug:category_slug>/', views.CategoryListView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CategoryListView.as_view(), name='product_list_by_category'),
    
    path('<slug:category_slug>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    

]
