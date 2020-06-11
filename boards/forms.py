from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext, gettext_lazy as _

from . import models


class PostCreationForm(forms.ModelForm):
    file = forms.FileField(error_messages={'required': 'Please provide an image!'})

    class Meta:
        model = models.Post
        fields = ['body', 'file', 'name', 'title']
        widgets = {
            'body': forms.Textarea(),
            'file': forms.FileInput(attrs={'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'placeholder': 'Anonymous'}),
        }


class ReplyCreationForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['board', 'body', 'file', 'ip_address', 'name', 'parent']
        widgets = {
            'body': forms.Textarea(),
            'file': forms.FileInput(attrs={'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'placeholder': 'Anonymous'}),
        }


class AdminBoardForm(forms.ModelForm):
    class Meta:
        model = models.Board
        exclude = ['created_at', 'updated_at']


class AdminPostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        exclude = ['created_at', 'file_delete_hash', 'file_height', 'file_name', 'file_size', 'file_url',
                   'file_width', 'ip_address', 'updated_at']
