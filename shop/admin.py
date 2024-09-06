from django.contrib import admin
from .models import Category, Product, Feedback



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',  'price', 'discount', 'quantyty','available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available','discount', 'quantyty',]
    search_fields = ["name", "description"]
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение слага


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('subject', 'first_name', 'phone_number', 'email', 'content')
