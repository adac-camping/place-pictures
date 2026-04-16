from django.contrib import admin

from image.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("prn", "name", "status", "tag_count", "is_main", "position", "updated_at")
    list_filter = ("status", "is_main")
    search_fields = ("prn", "name", "partner_id", "partner_campsite_id")
    ordering = ("prn", "position", "name")

    def tag_count(self, obj):
        return len(obj.tags or [])

    tag_count.short_description = "Tags"
