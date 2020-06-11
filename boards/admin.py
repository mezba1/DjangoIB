from django.contrib import admin

from . import forms
from . import models


class BoardAdmin(admin.ModelAdmin):
    form = forms.AdminBoardForm
    list_display = ['slug', 'title', 'is_sfw', 'created_at', 'updated_at']


class PostAdmin(admin.ModelAdmin):
    form = forms.AdminPostForm
    list_display = ['board', 'title', 'body', 'file_url', 'ip_address', 'is_archived', 'is_locked', 'is_sticky',
                    'user']


admin.site.register(models.Board, BoardAdmin)
admin.site.register(models.Post, PostAdmin)
