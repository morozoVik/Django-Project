from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Product
from .forms import ProductForm


class HomeView(ListView):
    """Главная страница с товарами"""
    model = Product
    template_name = "catalog/home.html"
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
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового товара"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара"""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:home')


class CategoriesView(ListView):
    """Страница со всеми категориями"""
    model = Category
    template_name = "catalog/categories.html"
    context_object_name = "categories"


class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса формы контактов"""
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(f"Новое сообщение от {name} ({phone}): {message}")
        return self.get(request, *args, **kwargs)