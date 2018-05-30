from django.contrib import admin
from tecqii.models import Tag, User, Item, UserTagRelation, UserKeyword

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'followers_count', 'icon_url', 'items_count')

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'followees_count', 'followers_count')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'likes_count')

class UserTagRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag', 'items_count', 'contribution_count')

class UserKeywordAdmin(admin.ModelAdmin):
    list_display = ('user', 'keyword', 'weight')

admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(UserTagRelation, UserTagRelationAdmin)
admin.site.register(UserKeyword, UserKeywordAdmin)