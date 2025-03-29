import uuid
import os
import random

from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.apps import apps


def generate_card_number():
    return str(random.randint(0, 99999999))

def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"

    return os.path.join('profile_image/', new_filename)


class User(AbstractUser):
    ROLES = (
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='student')
    classroom = models.CharField(max_length=10, blank=True, null=True, verbose_name="Класс")
    username = models.CharField(max_length=20, unique=True, blank=False)
    email = models.EmailField(max_length=20, unique=True, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    cover = models.ImageField(upload_to=rename_file, default="profile_image/default.png", blank=True)
    is_teacher = models.BooleanField(default=False)
    lesson_name = models.CharField(max_length=20, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.classroom})"

# class User

class Friendship(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидание"),
        ("accepted", "Принято"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests_sent")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests_received")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "friend")  # Запрещаем дублирование заявок

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username} ({self.status})"

    @staticmethod
    def add_friend(user, friend):
        if user != friend and not Friendship.objects.filter(user=user, friend=friend).exists():
            Friendship.objects.create(user=user, friend=friend)
            Friendship.objects.create(user=friend, friend=user)  # Двусторонняя связь

    @staticmethod
    def remove_friend(user, friend):
        Friendship.objects.filter(user=user, friend=friend).delete()
        Friendship.objects.filter(user=friend, friend=user).delete()

    @staticmethod
    def is_friend(user, friend):
        return Friendship.objects.filter(user=user, friend=friend).exists()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь с моделью User
    bio = models.TextField(blank=True, null=True)  # Биография пользователя
    avatar = models.ImageField(upload_to=rename_file, blank=True, null=True)  # Аватар
    birth_date = models.DateField(blank=True, null=True)  # Дата рождения

    def __str__(self):
        return f'{self.user.username} Profile'


class PrivacySettings(models.Model):
    PRIVACY_CHOICES = [
        (2, 'Для всех'),
        (1, 'Только друзья'),
        (0, 'Только я'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='privacy_settings')
    show_friends = models.IntegerField(choices=PRIVACY_CHOICES, default=2)
    show_grades = models.IntegerField(choices=PRIVACY_CHOICES, default=2)

    def __str__(self):
        return f"Настройки приватности {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile_and_card(sender, instance, created, **kwargs):
    if created:
        # Создание профиля
        Profile.objects.create(user=instance)

        SchoolCard = apps.get_model('school_card', 'SchoolCard')

        # Создание школьной карты
        SchoolCard.objects.create(
            user=instance,
            balance=0.00,
            card_number=generate_card_number()
        )

        PrivacySettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.schoolcard.save()
    instance.privacy_settings.save()
