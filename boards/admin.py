from django.contrib import admin

from . import forms
from . import models


class BoardAdmin(admin.ModelAdmin):
    add_form = forms.AdminBoardCreationForm
    form = forms.AdminBoardChangeForm
    list_display = ['slug', 'title', 'is_sfw', 'created_at', 'updated_at']


class PostAdmin(admin.ModelAdmin):
    add_form = forms.AdminPostCreationForm
    form = forms.AdminPostChangeForm
    list_display = ['board', 'title', 'body', 'file_url', 'ip_address', 'is_archived', 'is_locked', 'is_sticky',
                    'user']
    # readonly_fields = ['created_at', 'updated_at']


admin.site.register(models.Board, BoardAdmin)
admin.site.register(models.Post, PostAdmin)
