from django.contrib.sitemaps import Sitemap
from .models import Product
from django.urls import reverse_lazy


class ProductSitemaps(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated


class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        # return ['shop:index', 'shop:contacts']
        return ['shop:index']

    def location(self, item):
        return reverse_lazy(item)
