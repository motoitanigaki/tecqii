from django.contrib import admin
from tecqii.models import Tag, User

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'followers_count', 'icon_url', 'items_count')

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'followees_count', 'followers_count')

admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)