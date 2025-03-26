from django.db import models

# Create your models here.
class SchoolCard(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    card_number = models.CharField(max_length=8, unique=True)

class Transaction(models.Model):
    card = models.ForeignKey(SchoolCard, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)