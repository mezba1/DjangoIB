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


class AdminBoardCreationForm(forms.ModelForm):
    class Meta:
        model = models.Board
        # fields = ['file_delete_hash', 'file_height', 'file_size', 'file_url', 'file_width', 'updated_at']
        exclude = []


class AdminBoardChangeForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField(label=("Password"),
    #                                      help_text=("Raw passwords are not stored, so there is no way to see "
    #                                                 "this post's password, but you can change the password "
    #                                                 "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = models.Board
        exclude = []


class AdminPostCreationForm(forms.ModelForm):
    class Meta:
        model = models.Post
        # fields = ['file_delete_hash', 'file_height', 'file_size', 'file_url', 'file_width', 'updated_at']
        exclude = []


class AdminPostChangeForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField(label=("Password"),
    #                                      help_text=("Raw passwords are not stored, so there is no way to see "
    #                                                 "this post's password, but you can change the password "
    #                                                 "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = models.Post
        exclude = []
