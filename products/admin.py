#
#   file 	: products/admin.py
#	author	: andromeda
#   desc 	: Admin page config for product app
#
from django.contrib import admin

# Register your models here.

from .models import Product

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)