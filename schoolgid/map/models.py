from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50)  # "Кабинет 301"
    floor = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)  # "Кабинет физики"
    photo = models.ImageField(upload_to='map/', blank=True)