from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Product


class StaticViewSitemap(Sitemap):

	def items(self):
		return [ 'store', 'cart', 'checkout', 'contact', 'about',]

	def location(self, item):
		return reverse(item)

class ProductSitemap(Sitemap):

	def items(self):
		return Product.objects.all()