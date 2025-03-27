from rest_framework.routers import SimpleRouter
from . import views
from django.urls import path

router = SimpleRouter()
router.register(r'category_list', views.CategoryAPIViews, basename='category')
router.register(r'product_list_by_category', views.ProductListByCategoryAPIViews)
router.register(r'cart', views.CartAPIViews, basename='cart')
router.register(r'order', views.OrderAPIView, basename='order')
router.register(r'order_item', views.OrderItemView, basename='order_item')

urlpatterns = [ 
  path('post_code/', views.PostCodeAPIViev.as_view(), name='post_code'),
]



app_name = 'api'
urlpatterns += router.urls