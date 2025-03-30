from enum import unique

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Post


class AddPost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'news-add-title', 'placeholder': "Необязательно"}), label='', max_length=24, required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 25, 'cols': 80, 'class': 'news-add-text', 'placeholder': "Напишите что-нибудь"}), label="", required=True)
    cover = forms.ImageField(widget=forms.FileInput(attrs={'class': 'news-add-file-cover'}), label="", required=False)
    author = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'news-add-author'})  # Для стилизации
    )

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'cover',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем пользователя из views
        super().__init__(*args, **kwargs)

        if user:
            self.fields['author'].choices = [
                (str(user.id), f"От {user.first_name} {user.last_name}"),
                ('anonymous', 'От лица школы')
            ]