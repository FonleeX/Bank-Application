from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Transaction, TRANSACTION_TYPE_CHOICES, TRANSACTION_CATEGORY_CHOICES
from banking.models import BankAccount

User = get_user_model()

class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users for testing
        cls.user1 = User.objects.create(email='user1@example.com')
        cls.user2 = User.objects.create(email='user2@example.com')

        # Create bank accounts for testing
        cls.account1 = BankAccount.objects.create(
            user=cls.user1,
            account_type='Personal',
            account_number=11111111,
            account_sort_code=22222222,
            balance=1000.00
        )
        cls.account2 = BankAccount.objects.create(
            user=cls.user2,
            account_type='Personal',
            account_number=33333333,
            account_sort_code=44444444,
            balance=2000.00
        )

        # Create transactions for testing
        cls.transaction1 = Transaction.objects.create(
            account=cls.account1,
            amount=500.00,
            balance_after_transaction=1500.00,
            transaction_type=0,  # Incoming
            transaction_category=0,  # Deposit
            origin_account=None,
            destination_account=None
        )
        cls.transaction2 = Transaction.objects.create(
            account=cls.account1,
            amount=200.00,
            balance_after_transaction=1300.00,
            transaction_type=1,  # Outgoing
            transaction_category=2,  # Transfer
            origin_account=cls.account1,
            destination_account=cls.account2
        )

    def test_transaction_creation(self):
        # Test if transaction creation works as expected
        self.assertEqual(self.transaction1.account, self.account1)
        self.assertEqual(self.transaction1.amount, 500.00)
        self.assertEqual(self.transaction1.balance_after_transaction, 1500.00)
        self.assertEqual(self.transaction1.transaction_type, 0)
        self.assertEqual(self.transaction1.transaction_category, 0)
        self.assertIsNone(self.transaction1.origin_account)
        self.assertIsNone(self.transaction1.destination_account)

    def test_transaction_str_method(self):
        # Test the __str__ method of Transaction model
        expected_str = f"{self.transaction1.transaction_id} - {self.account1.account_number} - Deposit - 500.00"
        self.assertEqual(str(self.transaction1), expected_str)

    def test_transaction_choices(self):
        # Test if transaction type and category choices are as expected
        self.assertEqual(TRANSACTION_TYPE_CHOICES, ((0, 'Incoming'), (1, 'Outgoing')))
        self.assertEqual(TRANSACTION_CATEGORY_CHOICES, ((0, 'Deposit'), (1, 'Withdrawal'), (2, 'Transfer'), (3, 'Intrest'), (4, 'Loan')))
    
