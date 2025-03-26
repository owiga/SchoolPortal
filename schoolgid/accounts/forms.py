from enum import unique

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User, Profile


only_cyrillic = RegexValidator(
    regex=r'^[А-ЯЁа-яё]+$',
    message="Разрешены только буквы кириллицы."
)

class RegistrationForm(UserCreationForm):
    LETTERS = [
        ('А', 'А'),
        ('Б', 'Б'),
        ('В', 'В'),
        ('Г', 'Г'),
        ('Д', 'Д'),
        ('К', 'К'),
        ('Т', 'Т'),
    ]

    # Все возможные числа, чтобы Django их знал
    ALL_NUMBERS = [(str(i), str(i)) for i in range(1, 12)]  # 1-11 включительно

    classroom = forms.ChoiceField(
        label="Выберите букву и номер класса",
        choices=LETTERS,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'letter-select'}),
        required=True
    )
    number = forms.ChoiceField(
        label="",
        choices=ALL_NUMBERS,  # <-- СЮДА ДОБАВЛЯЕМ ВСЕ ЧИСЛА!
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'number-select', 'disabled': 'false'})
    )
    email = forms.EmailField(
        max_length=30,
        required=True,
        label="Электронная Почта*",
        help_text='',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите Почту'
        }),
    )
    cover = forms.ImageField(
        required=False,
        label="Фото профиля",
        widget=forms.FileInput(attrs={
            'id': 'reg-cover',
            'onchange': 'updateFileName()'
        })
    )

    username = forms.CharField(
        label="Логин*",
        widget=forms.TextInput(attrs={
            'placeholder': 'Придумайте Логин'
        }
        ),
        error_messages={
            "required": "Введите имя пользователя!",
            "max_length": "Имя пользователя не должно превышать 20 символов.",
            "unique": "Имя пользователя уже занято, попробуйте другое."
        }
    )

    password1 = forms.CharField(
        label='Пароль*',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Придумайте Пароль'
        }),
        help_text=''  # Убираем подсказку
    )

    first_name = forms.CharField(
        label='Имя - Фамилия*',
        widget=forms.TextInput(attrs={
            'class': 'register-fpi',
            'placeholder': 'Имя'
        }),
        validators=[only_cyrillic],
        help_text=''  # Убираем подсказку
    )

    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'register-fpi',
            'placeholder': 'Фамилия'
        }),
        validators=[only_cyrillic],
        help_text=''  # Убираем подсказку
    )

    password2 = forms.CharField(
        label='Подтверждение пароля*',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Потвердите Пароль'
        }),
        help_text=''  # Убираем подсказку
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'classroom',
            'number',
            'cover',
            'password1',
            'password2',
        )
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Данная почта уже привязана, попробуйте другую.")
        return email

class TeacherRegForm(UserCreationForm):
    classroom = forms.CharField(widget=forms.HiddenInput(), required=False, initial="Teacher")  # Скрытое поле
    number = forms.ChoiceField(widget=forms.HiddenInput(), required=False)
    email = forms.EmailField(
        max_length=30,
        required=True,
        label="Электронная Почта*",
        help_text='',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите Почту'
        }),
    )
    cover = forms.ImageField(
        required=False,
        label="Фото профиля",
        widget=forms.FileInput(attrs={
            'id': 'reg-cover',
            'onchange': 'updateFileName()'
        })
    )

    username = forms.CharField(
        label="Логин*",
        widget=forms.TextInput(attrs={
            'placeholder': 'Придумайте Логин'
        }
        ),
        error_messages={
            "required": "Введите имя пользователя!",
            "max_length": "Имя пользователя не должно превышать 20 символов.",
            "unique": "Имя пользователя уже занято, попробуйте другое."
        }
    )

    first_name = forms.CharField(
        label='Имя - Фамилия*',
        widget=forms.TextInput(attrs={
            'class': 'register-fpi',
            'placeholder': 'Имя'
        }),
        validators=[only_cyrillic],
        help_text=''  # Убираем подсказку
    )

    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'register-fpi',
            'placeholder': 'Фамилия'
        }),
        validators=[only_cyrillic],
        help_text=''  # Убираем подсказку
    )

    password1 = forms.CharField(
        label='Пароль*',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Придумайте Пароль'
        }),
        help_text=''  # Убираем подсказку
    )

    password2 = forms.CharField(
        label='Подтверждение пароля*',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Потвердите Пароль'
        }),
        help_text=''  # Убираем подсказку
    )

    lesson_name = forms.CharField(
        label="Что вы преподаёте?*",
        widget=forms.TextInput(attrs={
            'placeholder': 'Математика'
        }),
        help_text=''
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'cover',
            'password1',
            'password2',
            'lesson_name'
        )

    def save(self, commit=True):
        print(1)
        user = super().save(commit=False)
        user.is_teacher = True  # Указываем, что это учитель
        user.classroom = "0w2xs"
        user.role = "teacher"
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите ваш логин', 'class': 'login-input'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите ваш пароль', 'class': 'login-input'}), label="")

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']