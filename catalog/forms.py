from django import forms
from django.core.exceptions import ValidationError
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для продукта с валидацией запрещенных слов и цены"""

    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с добавлением CSS-классов"""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'status':
                field.widget.attrs['class'] = 'form-control'

            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название товара'
                field.widget.attrs['autofocus'] = 'autofocus'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание товара'
                field.widget.attrs['rows'] = '4'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = '0.00'
                field.widget.attrs['min'] = '0.01'
                field.widget.attrs['step'] = '0.01'

            field.widget.attrs['aria-label'] = f'Поле {field.label.lower()}'

        self.fields['description'].widget.attrs['class'] += ' form-control-lg'
        self.fields['price'].widget.attrs['class'] += ' text-success fw-bold'
        self.fields['image'].widget.attrs['class'] += ' form-control-file'
        self.fields['category'].widget.attrs['class'] += ' form-select'

        self.fields['name'].label = 'Название товара'
        self.fields['description'].label = 'Описание товара'
        self.fields['image'].label = 'Изображение товара'
        self.fields['category'].label = 'Категория'
        self.fields['price'].label = 'Цена товара (руб.)'

        if 'status' in self.fields:
            self.fields['status'].label = 'Статус публикации'
            self.fields['status'].help_text = 'Выберите статус видимости продукта'

        self.fields['price'].help_text = 'Введите положительное значение цены'
        self.fields['name'].help_text = 'Название должно быть уникальным и информативным'
        self.fields['description'].help_text = 'Подробно опишите характеристики товара'

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data['name'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(
                    f'Название содержит запрещенное слово: "{word}". '
                    f'Использование слов {", ".join(self.FORBIDDEN_WORDS)} запрещено.'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания продукта"""
        description = self.cleaned_data.get('description', '').lower()

        if description:
            for word in self.FORBIDDEN_WORDS:
                if word in description:
                    raise ValidationError(
                        f'Описание содержит запрещенное слово: "{word}". '
                        f'Использование слов {", ".join(self.FORBIDDEN_WORDS)} запрещено.'
                    )

        return self.cleaned_data['description']

    def clean_price(self):
        """Кастомная валидация цены продукта"""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной. '
                'Пожалуйста, введите положительное значение.'
            )

        if price == 0:
            raise ValidationError(
                'Цена не может быть нулевой. '
                'Пожалуйста, введите положительное значение.'
            )

        return price