from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import models


from .models import Category, Product
from .forms import ProductForm


class HomeView(ListView):
    """Главная страница с товарами"""
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(
                models.Q(status='published') |
                models.Q(owner=self.request.user)
            ).distinct()
        return queryset.filter(status='published')

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
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Товар успешно создан!')
        return super().form_valid(form)


class IsOwnerOrModeratorMixin(UserPassesTestMixin):
    """ Миксин для проверки прав владельца или модератора"""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        obj = self.get_object()

        if obj.owner == self.request.user:
            return True

        if self.request.user.has_perm('catalog.delete_product'):
            return True

        return False

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для выполнения этого действия!')
        return redirect('catalog:product_detail', pk=self.get_object().pk)


class IsOwnerMixin(UserPassesTestMixin):
    """ Миксин для проверки, что пользователь - владелец продукта"""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        obj = self.get_object()
        return obj.owner == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете редактировать только свои товары!')
        return redirect('catalog:product_detail', pk=self.get_object().pk)


class ProductUpdateView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    """Редактирование товара - только владелец"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        messages.success(self.request, 'Товар успешно обновлен!')
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.has_perm('catalog.can_change_product_status'):
            if 'status' in form.fields:
                del form.fields['status']
        return form


class ProductDeleteView(LoginRequiredMixin, IsOwnerOrModeratorMixin, DeleteView):
    """Удаление товара - владелец или модератор"""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:home')
    login_url = reverse_lazy('users:login')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(self.request, f'Товар "{product.name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


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
            messages.success(request, 'Сообщение успешно отправлено!')
        return self.get(request, *args, **kwargs)


class CategoryProductsView(ListView):
    """Страница с товарами конкретной категории"""
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        self.category = get_object_or_404(Category, id=category_id)

        queryset = Product.objects.filter(category=self.category)

        if self.request.user.is_authenticated:
            return queryset.filter(
                models.Q(status='published') |
                models.Q(owner=self.request.user)
            ).distinct()
        return queryset.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        for product in context['products']:
            if product.description and len(product.description) > 100:
                product.short_description = product.description[:100] + '...'
            else:
                product.short_description = product.description or 'Описание отсутствует'
        return context


@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    """Снятие продукта с публикации - только модератор"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.status = 'draft'
        product.save()
        messages.success(request, f'Продукт "{product.name}" снят с публикации')
        return redirect('catalog:product_detail', pk=product.pk)

    return render(request, 'catalog/product_unpublish.html', {'product': product})


@login_required
@permission_required('catalog.can_change_product_status', raise_exception=True)
def change_product_status(request, pk, status):
    """Изменение статуса продукта - только модератор"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        if status in ['draft', 'published', 'rejected']:
            old_status = product.get_status_display()
            product.status = status
            product.save()
            new_status = product.get_status_display()
            messages.success(
                request,
                f'Статус продукта "{product.name}" изменен с "{old_status}" на "{new_status}"'
            )
        return redirect('catalog:product_detail', pk=product.pk)

    return render(request, 'catalog/product_change_status.html', {
        'product': product,
        'status': status,
        'status_display': dict(Product.STATUS_CHOICES).get(status, 'Неизвестный статус')
    })