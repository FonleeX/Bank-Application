from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length = 254, null=False, blank=False)
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
    
    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return 0

class BankAccountType(models.Model):
    name = models.CharField(max_length=128)
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='Interest rate from 0 - 100'
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text='The number of times interest will be calculated per year'
    )

    def __str__(self):
        return self.name
    
    def calculate_interest(self, principal):
        p = principal
        r = self.annual_interest_rate
        n = Decimal(self.interest_calculation_per_year)
        interest = (p * (1 + ((r/100) / n))) - p
        return round(interest, 2)

class BankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    #account_type = models.CharField(max_length = 32, default="Personal")
    account_type = models.ForeignKey(
        BankAccountType,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_number = models.PositiveIntegerField(unique=True)
    account_sort_code = models.PositiveIntegerField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    interest_start_date = models.DateField(
        null=True, blank=True,
        help_text=(
            'The month number that interest calculation will start from'
        )
    )
    initial_deposit_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.account_number)
    
    def get_interest_calculation_months(self):
        # List of month numbers that interest will be calculated for
        # e.g. [2,4,6,8,10,12] for 2 month intervals

        interval = int(
            12 / self.account_type.interest_calculation_per_year
        )
        start = self.interest_start_date.month
        return [i for i in range(start, 13 interval)]
    
class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address'
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email