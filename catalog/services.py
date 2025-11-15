from django.core.cache import cache
from django.conf import settings
from django.db import models
from .models import Product


def get_products_by_category(category_id):
    """
    Сервисная функция для получения продуктов по категории с кешированием
    """
    cache_key = f'products_category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(
            category_id=category_id,
            status='published'
        ).select_related('category', 'owner')

        if settings.CACHE_ENABLED:
            cache.set(cache_key, products, timeout=300)

    return products


def get_categories_with_products():
    """
    Сервисная функция для получения категорий с количеством продуктов
    """
    cache_key = 'categories_with_counts'
    categories = cache.get(cache_key)

    if categories is None:
        from .models import Category
        categories = Category.objects.annotate(
            product_count=models.Count('product', filter=models.Q(product__status='published'))
        )

        if settings.CACHE_ENABLED:
            cache.set(cache_key, categories, timeout=600)

    return categories