from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',  'subcategory' ,'veg_or_Nonveg', 'price')  # Fields to display in the admin list view
    search_fields = ('name','category__name','subcategory__name')  # Add fields for searching in the admin panel


    
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product,ProductAdmin)