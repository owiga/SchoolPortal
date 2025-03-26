from django.db import models
from django.conf import settings

class Grade(models.Model):
    student = models.ForeignKey(
        'accounts.User',  # Ссылка через строку!
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    lesson = models.CharField(max_length=25)
    value = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=False)
    comment = models.CharField(max_length=100)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_account_id")