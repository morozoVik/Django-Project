from django.db import models


class BlogPost(models.Model):
    """Модель блоговой записи"""

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Введите заголовок статьи"
    )

    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите текст статьи"
    )

    preview = models.ImageField(
        upload_to="blog/",
        verbose_name="Превью",
        help_text="Загрузите изображение для превью",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Отметьте для публикации статьи"
    )

    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title