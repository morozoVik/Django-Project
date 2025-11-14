from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class Category(models.Model):
    """Модель для категорий товаров"""

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель для товаров"""

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]

    name = models.CharField(
        max_length=100, verbose_name="Наименование", help_text="Введите название товара"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание товара",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение",
        help_text="Загрузите изображение товара",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию товара",
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
        help_text="Введите цену товара",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        help_text="Владелец продукта",
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус публикации"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]
        permissions = [
            ("can_edit_description", "Can edit product description"),
            ("can_edit_category", "Can edit product category"),
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_product_status", "Может изменять статус продукта"),
        ]

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    def is_published(self):
        return self.status == 'published'

    def clean(self):
        """Валидация запрещенных слов"""
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        # Проверяем название и описание
        fields_to_check = {
            'name': self.name,
            'description': self.description
        }

        for field_name, field_value in fields_to_check.items():
            if field_value:
                text = field_value.lower()
                for word in forbidden_words:
                    if re.search(rf'\b{word}\b', text):
                        raise ValidationError(
                            f'Поле "{self._meta.get_field(field_name).verbose_name}" содержит запрещенное слово: "{word}"'
                        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)