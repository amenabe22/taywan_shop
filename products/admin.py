from django.contrib import admin
from .models import Product, Category, Tag, Color, ParentCategory


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'price', 'available_in',
                    'trending', 'featured', 'in_stock', 'timestamp',)
    list_editable = ('title', 'price', 'available_in',
                     'featured', 'in_stock', 'trending',)
    list_display_links = ('id',)
    search_fields = ('title','tags__tag',)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Color)
admin.site.register(ParentCategory)
admin.site.register(Product, ProductsAdmin)
