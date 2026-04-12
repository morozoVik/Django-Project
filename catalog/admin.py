from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для категорий"""

    list_display = ("id", "name", "description")
    list_filter = ("name",)
    list_display_links = ("id", "name")
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для товаров"""

    list_display = ("id", "name", "category", "price", "created_at", "updated_at")
    list_display_links = ("id", "name")
    list_filter = ("category", "created_at", "updated_at")
    list_editable = ("price",)
    search_fields = ("name", "description", "category__name")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("name", "description", "image", "category")},
        ),
        ("Финансовая информация", {"fields": ("price",)}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
