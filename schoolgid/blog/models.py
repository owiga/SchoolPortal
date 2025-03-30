import os, uuid

from django.conf import settings
from django.db import models
from accounts.models import User


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    print(instance)
    new_filename = f"{uuid.uuid4().hex}.{ext}"

    return os.path.join('posts/', new_filename)


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    cover = models.ImageField(upload_to=rename_file, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        """Возвращает общее количество лайков для поста"""
        return self.likes.count()

    def user_liked_post(self, user):
        """Проверяет, лайкнул ли данный пользователь этот пост"""
        return self.likes.filter(user=user).exists()


class Logo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='general/')  # Изображения будут сохраняться в media/products/

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Убедимся, что пользователь может поставить только один лайк на пост

    def __str__(self):
        return f"{self.user.username} liked {self.blog.post.title}"