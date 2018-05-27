from django.contrib import admin
from tecqii.models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'followers_count', 'icon_url', 'items_count')

admin.site.register(Tag, TagAdmin)