from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'contact', 'products', 'special_offers']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
