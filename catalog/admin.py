from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для категорий"""
    list_display = ('id', 'name', 'description')  # Что в списке
    list_filter = ('name',)  # Фильтры справа
    search_fields = ('name', 'description')  # Поля для поиска


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для товаров"""
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'created_at',
        'updated_at'
    )
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'category__name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image', 'category')
        }),
        ('Финансовая информация', {
            'fields': ('price',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )