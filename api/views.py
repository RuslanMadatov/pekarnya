from rest_framework import viewsets, permissions, mixins
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .serializers import CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer, PostCodeSerializer, OrderItemSerializer
from shop.models import Category, Product
from cart.models import Cart
from orders.models import Order, OrderItem, PostCode
from payment.views import payment_process_api 
from .filters import  ProductListByCategoryAndFilter

# создает список категорий для меню(только чтение)
class CategoryAPIViews(viewsets.ReadOnlyModelViewSet):
  permission_classes = (permissions.AllowAny,)
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  
# выводит список продуктов по категории, детальную информацию о продукте и фильтрация продуктов(только чтение)
class ProductListByCategoryAPIViews(viewsets.ReadOnlyModelViewSet):
     permission_classes = (permissions.AllowAny,)
     queryset = Product.objects.all()
     serializer_class = ProductSerializer
     filterset_class = ProductListByCategoryAndFilter


# выводит список корзин покупателя, фильтр по user (все действия)
class CartAPIViews(viewsets.ModelViewSet):
    serializer_class = CartSerializer
            
    def get_queryset(self):
        queriset = Cart.objects.all()
        user = self.request.user
        if user:
            queriset = queriset.filter(user=user)   
        else:
            queriset = None
        return queriset

                   
# выводит список Заказов покупателя, фильтр по user (все действия), а также инициализирует оплату
class OrderAPIView(mixins.CreateModelMixin,
                  #  mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    
    serializer_class = OrderSerializer

    def get_queryset(self):
        queriset = Order.objects.all()
        user = self.request.user
        if user:
            queriset = queriset.filter(user=user, paid=False)            
        else:
            queriset = None       
        return queriset
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        user=User.objects.get(username=request.user)
        user_id = user.id
        order = Order.objects.get(user=user_id, paid=False)
        order_id = order.pk
        cart_price = order.get_total_cost()
        return HttpResponseRedirect(payment_process_api(cart_price, order_id, request))

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        user=User.objects.get(username=request.user)
        user_id = user.id
        order = Order.objects.get(user=user_id, paid=False)
        order_id = order.pk
        cart_price = order.get_total_cost()
        return HttpResponseRedirect(payment_process_api(cart_price, order_id, request))

# выводит список элементов заказов юзера
class OrderItemView(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        queriset = OrderItem.objects.all()
        user = self.request.user
        if user:
            queriset = queriset.filter(user=user)   
        else:
            queriset = None
        return queriset


#  проверяет статус посылки через POST-запрос от клиента
class PostCodeAPIViev(APIView):
    
    def post(self, request, format=None):
        code = request.data['code']
        #  чтобы не выводилась ошибка DoesNotExist
        try:
          # проверяем существет ли в БД ordrer_code
          code_order = PostCode.objects.get(order_code=code)
          serializer = PostCodeSerializer(code_order)
          return Response(serializer.data)
        except (ValueError, ObjectDoesNotExist):
            #  если нет отправляем сообщение
            data = {'message': 'Проверьте Ваш код'}
            return Response(data, status=406 )
    