from django.contrib import admin

from .models import Category, Product, Ingredient

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Ingredient)
