from django.contrib import admin
from django.utils.html import format_html
from .models import Category, MediaItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ["preview", "title", "kind", "category", "featured", "is_published", "views", "created"]
    list_display_links = ["preview", "title"]
    list_editable = ["featured", "is_published"]
    list_filter = ["kind", "category", "is_published", "featured"]
    search_fields = ["title", "description"]
    date_hierarchy = "created"

    @admin.display(description="معاينة")
    def preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="height:44px;width:64px;object-fit:cover;border-radius:6px">', obj.cover.url)
        return "—"
