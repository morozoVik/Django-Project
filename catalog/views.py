from django.shortcuts import render

from .models import Category, Product


def home(request):
    """Главная страница с товарами"""
    products = Product.objects.all()

    return render(request, "home.html", {"products": products})


def contacts(request):
    """Страница контактов"""
    return render(request, "contacts.html")


def product_detail(request, product_id):
    """Страница одного товара"""
    product = Product.objects.get(id=product_id)
    return render(request, "product_detail.html", {"product": product})


def categories(request):
    """Страница со всеми категориями"""
    categories_list = Category.objects.all()
    return render(request, "categories.html", {"categories": categories_list})
