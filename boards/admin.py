from django.contrib import admin

from . import forms
from . import models


def make_archived(_, __, queryset):
    queryset.update(is_archived=True)


def make_locked(_, __, queryset):
    queryset.update(is_locked=True)


def make_sticky(_, __, queryset):
    queryset.update(is_sticky=True)


make_archived.short_description = "Mark selected threads as archived"
make_locked.short_description = "Mark selected threads as locked"
make_sticky.short_description = "Mark selected threads as sticky"


class BoardAdmin(admin.ModelAdmin):
    form = forms.AdminBoardForm
    list_display = ['slug', 'title', 'is_sfw', 'created_at', 'updated_at']


class PostAdmin(admin.ModelAdmin):
    actions = [make_archived, make_locked, make_sticky]
    form = forms.AdminPostForm
    list_display = ['is_thread', 'board', 'title', 'body', 'file_url', 'ip_address', 'is_archived', 'is_locked',
                    'is_sticky', 'user']

    def is_thread(self, obj):
        if obj.parent:
            return False
        else:
            return True

    is_thread.boolean = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            common_readonly = ['board', 'body', 'file', 'name', 'parent', 'quoted_posts', 'title', 'user']
            if obj.parent:
                return ['is_archived', 'is_locked', 'is_sticky'] + common_readonly
            else:
                return common_readonly
        else:
            return []


admin.site.register(models.Board, BoardAdmin)
admin.site.register(models.Post, PostAdmin)
