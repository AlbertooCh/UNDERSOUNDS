from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.
class User(AbstractUser):
    credit_card_number = models.CharField(
        max_length=16,
        null=True,  # Permite NULL en la base de datos
        blank=True,  # Permite campo vacío en formularios
        default=None,  # Valor por defecto explícito
        verbose_name='Número de tarjeta'
    )
    credit_card_expiry = models.DateField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Fecha de expiración'
    )
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    pass
