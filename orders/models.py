from django.db import models
from django.contrib.auth.models import User

from shop.models import Product
from cart.models import Cart


class OrderitemQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    # поле user,т. к. только аутентифицированый пользователь может взаимодействовать с DRF и токенами 
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    # если что изменить session_key на Forengekey от Session
    session_key = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField()
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    text = models.CharField(blank=True, max_length=700, verbose_name = 'Пожелания к заказу')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления заказа')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    y_cassa_id = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created']), ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    # выводит сумму покупок
    def get_total_cost(self):
        if self.user:
          carts = Cart.objects.filter(user=self.user).total_price()          
        else:
            carts = Cart.objects.filter(session_key=self.session_key).total_price()
        # return sum(cart.products_price() for cart in self)
        return carts


class OrderItem(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.SET_DEFAULT, default='Продукт удален')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=1, verbose_name='Скидка в %')
    

    class Meta:
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)

    def __str__(self):
        return str(self.id)

    objects = OrderitemQueryset.as_manager()

    def sell_price_order_item(self):
        if self.discount:         
            return round(self.price - self.price*self.discount/100, 2)
        return self.price

    def products_price(self):
        return round(self.sell_price_order_item() * self.quantity, 2)

    

#  статуса посылки
class PostCode(models.Model):
    CHOICES = (
        ('1', 'Заказ принят'),
        ('2', 'Заказ отправлен по почте'),
        ('3', 'Заказ прибыл'),
        ('4', 'Заказ взят клиентом'),        
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key = True)
    # post_code добавлется потом при отправки почты и получением кода посылки
    post_code = models.CharField(max_length=100, blank=True, verbose_name='Код почты')
    order_code = models.CharField(max_length=10, blank=True, verbose_name='Ключ')
    status = models.CharField(max_length=50, blank=True, choices = CHOICES, default = '1',verbose_name='Статус посылки')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')

    class Meta:
            verbose_name = 'Почтовый код'
            verbose_name_plural = 'Почтовые коды'