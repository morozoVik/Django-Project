from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми продуктами и категориями"

    def handle(self, *args, **options):
        # Очищаем базу данных
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write("База данных очищена")

        # Создаем категории
        categories_data = [
            {"name": "Плагины", "description": "Полезные плагины для различных систем"},
            {"name": "Телеграм боты", "description": "Боты для Telegram"},
            {"name": "Веб-приложения", "description": "Готовые веб-приложения"},
        ]

        categories = {}
        for data in categories_data:
            category = Category.objects.create(
                name=data["name"], description=data["description"]
            )
            categories[data["name"]] = category
            self.stdout.write(f"Создана категория: {category.name}")

        # Создаем продукты
        products_data = [
            {
                "name": "Плагин для рассылок",
                "description": "Плагин для email рассылок",
                "price": 2999.99,
                "category": "Плагины",
            },
            {
                "name": "Плагин для SEO",
                "description": "Плагин для SEO оптимизации",
                "price": 5999.00,
                "category": "Плагины",
            },
            {
                "name": "ТГ Бот уведомлений",
                "description": "Бот для уведомлений в Telegram",
                "price": 4999.50,
                "category": "Телеграм боты",
            },
            {
                "name": "Бот для заказов",
                "description": "Бот для автоматизации заказов",
                "price": 8999.00,
                "category": "Телеграм боты",
            },
            {
                "name": "Интернет-магазин",
                "description": "Готовый интернет-магазин на Django",
                "price": 14999.00,
                "category": "Веб-приложения",
            },
            {
                "name": "Корпоративный портал",
                "description": "Веб-приложение портала",
                "price": 24999.00,
                "category": "Веб-приложения",
            },
        ]

        for data in products_data:
            product = Product.objects.create(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                category=categories[data["category"]],
            )
            self.stdout.write(f"Создан продукт: {product.name} - {product.price} руб.")

        self.stdout.write("Готово!")
        self.stdout.write(f"Создано категорий: {Category.objects.count()}")
        self.stdout.write(f"Создано продуктов: {Product.objects.count()}")
