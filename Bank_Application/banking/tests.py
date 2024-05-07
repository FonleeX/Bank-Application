from django.test import TestCase
from .models import User, BankAccount
from transaction.models import Transaction
# Create your tests here.
"""
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
"""

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')

class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.bank_account = BankAccount.objects.create(
            user=self.user,
            account_number='1234567890',
            balance=1000,
            account_sort_code='123456'
        )
        self.transaction = Transaction.objects.create(
            account=self.bank_account,
            amount=100,
            balance_after_transaction=900, 
            transaction_type=1,  # Example transaction type
            transaction_category=1,  # Example transaction category
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.account, self.bank_account)
        self.assertEqual(self.transaction.amount, 100)

                