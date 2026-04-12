from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы и назначает права для модераторов продуктов'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Product)

        permissions = [
            'can_unpublish_product',
            'can_change_product_status',
            'delete_product',
            'change_product',
            'view_product',
            'can_edit_description',
            'can_edit_category',
        ]

        permission_objects = []
        for perm_codename in permissions:
            try:
                perm = Permission.objects.get(
                    codename=perm_codename,
                    content_type=content_type
                )
                permission_objects.append(perm)
                self.stdout.write(f'Найдено разрешение: {perm_codename}')
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Разрешение не найдено: {perm_codename}')
                )

        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        moderator_group.permissions.set(permission_objects)

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" создана успешно!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" обновлена успешно!')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Назначено прав: {moderator_group.permissions.count()}')
        )

        for perm in moderator_group.permissions.all():
            self.stdout.write(f' - {perm.name}')