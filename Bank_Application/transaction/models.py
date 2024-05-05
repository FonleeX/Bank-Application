from django.db import models
import uuid
from banking.models import BankAccount

TRANSACTION_TYPE_CHOICES = (
        (0, 'Incoming'),
        (1, 'Outgoing')
    )

TRANSACTION_CATEGORY_CHOICES = (
        (0, 'Deposit'),
        (1, 'Withdrawal'),
        (2, 'Transfer'),
        (3, 'Intrest'),
        (4, 'Loan')
    )

class Transaction(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

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

    transaction_category = models.PositiveSmallIntegerField(
        choices=TRANSACTION_CATEGORY_CHOICES
    )

    origin_account = models.ForeignKey(
        'banking.BankAccount',
        null=True,
        blank=True,
        related_name='origin_transactions',
        on_delete=models.SET_NULL,
    )

    destination_account = models.ForeignKey(
        'banking.BankAccount',
        null=True,
        blank=True,
        related_name='destination_transactions',
        on_delete=models.SET_NULL,
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.transaction_id} - {self.account.account_number} - {self.category.name} - {self.amount}"

    class Meta:
        ordering = ['timestamp']