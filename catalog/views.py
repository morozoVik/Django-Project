from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView, TemplateView

from .models import Category, Product


class HomeView(ListView):
    """Главная страница с товарами"""
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['products']:
            if product.description and len(product.description) > 100:
                product.short_description = product.description[:100] + '...'
            else:
                product.short_description = product.description or 'Описание отсутствует'
        return context


class ProductDetailView(DetailView):
    """Страница одного товара"""
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class CategoriesView(ListView):
    """Страница со всеми категориями"""
    model = Category
    template_name = "categories.html"
    context_object_name = "categories"


class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = "contacts.html"

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса формы контактов"""
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            # Здесь можно добавить сохранение в БД или отправку email
            print(f"Новое сообщение от {name} ({phone}): {message}")
            # В реальном проекте здесь была бы логика обработки формы
        return self.get(request, *args, **kwargs)

# def home(request):
#     """Главная страница с товарами"""
#     products = Product.objects.all()
#
#     for product in products:
#         if product.description and len(product.description) > 100:
#             product.short_description = product.description[:100] + '...'
#         else:
#             product.short_description = product.description or 'Описание отсутствует'
#
#     return render(request, "home.html", {"products": products})
#
#
# def contacts(request):
#     """Страница контактов"""
#     return render(request, "contacts.html")
#
#
# def product_detail(request, pk):
#     """Страница одного товара"""
#     product = get_object_or_404(Product, id=pk)
#     return render(request, "product_detail.html", {"product": product})
#
#
# def categories(request):
#     """Страница со всеми категориями"""
#     categories_list = Category.objects.all()
#     return render(request, "categories.html", {"categories": categories_list})
