import csv
import datetime
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Order, OrderItem, TextArea, PostCode


# экспорт в csv
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
        field.many_to_many and not field.one_to_many]
    # записать первую строку с информацией заголовка
    writer.writerow([field.verbose_name for field in fields if field.name != 'session_key'])
    # записать строки данных
    for obj in queryset:
        data_row = []
        for field in fields:
            if field.name == 'session_key':
                continue
            else:
                value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Экспорт в CSV'


# для отображения html-версии
def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class TextAreaInline(admin.TabularInline):
    model = TextArea
    fields = ['text']

class PostCodeInline(admin.TabularInline):
    model = PostCode
    fields = ['post_code', 'order_code', 'status']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_key', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'paid',
                    'created',
                    'updated', 'y_cassa_id']
    list_filter = ['paid', 'created', 'updated']
    inlines = [TextAreaInline, OrderItemInline, PostCodeInline]
    actions = [export_to_csv]
