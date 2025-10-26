from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published", "views_count")
    list_filter = ("is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title", "content")
    readonly_fields = ("views_count", "created_at")