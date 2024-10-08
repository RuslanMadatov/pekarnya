from django.db import models
from shop.models import Product


class Order(models.Model):
    # если что изменить session_key на Forengekey от Session
    session_key = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField()
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
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

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.SET_DEFAULT, default='Продукт удален')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
    

# строка дополнительные пожелания при заказе товара
class TextArea(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key = True)
    text = models.CharField(blank=True, max_length=700)

    class Meta:
        verbose_name = 'Дополнение к заказу'

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

    class Meta:
            verbose_name = 'Почтовый код'
            verbose_name_plural = 'Почтовые коды'