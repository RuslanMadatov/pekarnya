from django.db import models
from django.urls import reverse_lazy
from phonenumber_field.modelfields import PhoneNumberField


# категории товаров
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название категории')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']), ]
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('shop:product_list_by_category', args=[self.slug])

# продукты в категории
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Фотография товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    available = models.BooleanField(default=True, verbose_name='Наличие товара')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания товара')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата и время последнего изменения товара')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=1, verbose_name='Скидка в %')
    new = models.BooleanField(default=False, verbose_name='Новый продукт')
    quantyty = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['id', 'slug']), models.Index(fields=['name']),
                   models.Index(fields=['-created']), ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('shop:product_detail', kwargs={'category_slug': self.category.slug, 'slug': self.slug})
    
    # проверка есть ли у товара скидка, если нет пишем просто цену
    def sell_price(self):
        if self.discount:         
            return round(self.price - self.price*self.discount/100, 2)
        return self.price
    
    
    
    

# лучше сделать отдельно, а не в shop
class Feedback(models.Model):
    """
    Модель обратной связи
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    phone_number = PhoneNumberField(verbose_name='Номер телефона')
    email = models.EmailField(max_length=255)
    content = models.TextField(blank=True, verbose_name='Содержимое письма')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']
        db_table = 'app_feedback'
