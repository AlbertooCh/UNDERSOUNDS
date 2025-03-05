from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    credit_card_number = models.CharField(max_length=16)
    credit_card_expiry = models.DateField()

