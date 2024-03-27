from django.db import models

from .constants import TRANSACTION_TYPE_CHOICES
from banking.models import BankAccount

class Transaction(models.Model):
    account = models.ForeignKey(
        BankAccount,
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.account.account_number)
    
    class Meta:
        ordering = ['timestamp']
