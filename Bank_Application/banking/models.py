from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length = 254)
    middle_name = models.CharField(max_length=100, null=True,)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    city = models.CharField(max_length = 64, default="Lincoln")
    address = models.CharField(max_length=200, default="Brayford Pool")
    postcode = models.CharField(max_length=8, default="LN6 7TS")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class BankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_type = models.CharField(max_length = 32, default="Personal")
    account_number = models.PositiveIntegerField(unique=True)
    account_sort_code = models.PositiveIntegerField(unique=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )