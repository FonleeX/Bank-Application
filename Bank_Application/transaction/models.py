from django.db import models
from banking.models import BankAccount

class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('INTEREST', 'Interest'),
    )


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
        max_digits=12,
        decimal_places=2
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return str(self.account.account_number)

    class Meta:
        ordering = ['timestamp']