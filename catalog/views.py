from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def home(request):
    """Главная страница с товарами"""
    products = Product.objects.all()

    for product in products:
        if product.description and len(product.description) > 100:
            product.short_description = product.description[:100] + '...'
        else:
            product.short_description = product.description or 'Описание отсутствует'

    return render(request, "home.html", {"products": products})


def contacts(request):
    """Страница контактов"""
    return render(request, "contacts.html")


def product_detail(request, pk):
    """Страница одного товара"""
    product = get_object_or_404(Product, id=pk)
    return render(request, "product_detail.html", {"product": product})


def categories(request):
    """Страница со всеми категориями"""
    categories_list = Category.objects.all()
    return render(request, "categories.html", {"categories": categories_list})
