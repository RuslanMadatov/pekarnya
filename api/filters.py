import django_filters

from shop.models import Product
from orders.models import PostCode

# фильтр по категории продуктов,существованию продукта, количеству товара, скидки и упорядочивания по цене
class ProductListByCategoryAndFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__name",
        lookup_expr="icontains",
        label="Поиск продукта по категории",
    )

    available = django_filters.BooleanFilter(field_name="available")
    quantyty = django_filters.NumberFilter(
        field_name="quantyty ", lookup_expr="gt", label="Количество товара"
    )
    new = django_filters.BooleanFilter(field_name="new")
    discount = django_filters.NumberFilter(
        field_name="discount", lookup_expr="gte", label="Скидка в %"
    )
    order_by = django_filters.OrderingFilter(
        fields=("price", "price"),
    )

    class Meta:
        model = Product
        fields = ["category", "available", "quantyty", "new", "discount", "price"]


        
