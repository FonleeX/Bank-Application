from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import BankAccount

User = get_user_model()

class BankAccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        cls.user = User.objects.create(email='test@example.com')

        # Create a bank account for the user
        cls.bank_account = BankAccount.objects.create(
            user=cls.user,
            account_type='Personal',
            account_number=12345678,
            account_sort_code=87654321,
            balance=1000.00
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')

    def test_bank_account_creation(self):
        self.assertEqual(self.bank_account.user, self.user)
        self.assertEqual(self.bank_account.account_type, 'Personal')
        self.assertEqual(self.bank_account.account_number, 12345678)
        self.assertEqual(self.bank_account.account_sort_code, 87654321)
        self.assertEqual(self.bank_account.balance, 1000.00)

    def test_balance_update(self):
        # Test updating balance
        self.bank_account.balance += 500.50
        self.bank_account.save()
        self.assertEqual(self.bank_account.balance, 1500.50)

    def test_account_number_uniqueness(self):
        # Test uniqueness of account number
        with self.assertRaises(Exception):
            BankAccount.objects.create(
                user=self.user,
                account_type='Business',
                account_number=12345678,  # This should raise an exception
                account_sort_code=12345678,
                balance=2000.00
            )

    def test_account_sort_code_uniqueness(self):
        # Test uniqueness of account sort code
        with self.assertRaises(Exception):
            BankAccount.objects.create(
                user=self.user,
                account_type='Business',
                account_number=87654321,
                account_sort_code=87654321,  # This should raise an exception
                balance=2000.00
            )
















































#from django.test import TestCase
#from banking.models import User, BankAccount
#from transaction.models import Transaction, TRANSACTION_TYPE_CHOICES, TRANSACTION_CATEGORY_CHOICES
#from decimal import Decimal
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

#class UserModelTestCase(TestCase):
#    def setUp(self):
#        self.user = User.objects.create(email='test@example.com')

#    def test_user_creation(self):
#        self.assertEqual(self.user.email, 'test@example.com')

#class TransactionModelTestCase(TestCase):
#    def setUp(self):
#        self.user = User.objects.create(email='test@example.com')
#        self.bank_account = BankAccount.objects.create(
#            user=self.user,
#            account_number='1234567890',
#            balance=1000,
#            account_sort_code='123456'
#        )

#    def test_transaction_creation(self):
        # Test creating transactions with different types and categories
#        transaction = Transaction.objects.create(
#            account=self.bank_account,
#            amount=100,
#            balance_after_transaction=900, 
#            transaction_type=0,  # Example transaction type (0 for Incoming)
#            transaction_category=0  # Example transaction category (0 for Deposit)
#        )
#        self.assertEqual(transaction.transaction_type, 0)  # Ensure transaction type is set correctly
#        self.assertEqual(transaction.transaction_category, 0)  # Ensure transaction category is set correctly

        # Test transaction amount and balance update
#        initial_balance = self.bank_account.balance
#        transaction = Transaction.objects.create(
#            account=self.bank_account,
#            amount=50,
#            balance_after_transaction=initial_balance - 50,  # Update balance after transaction
#            transaction_type=1,
#            transaction_category=1
#        )
    
        # Retrieve the updated balance after the transaction
#        updated_balance = BankAccount.objects.get(pk=self.bank_account.pk).balance
    
        # Debugging statements
#        print("Initial balance:", initial_balance)
#        print("Actual balance after transaction:", updated_balance)
    
#        self.assertEqual(transaction.amount, Decimal('50'))  # Compare amount as Decimal
#        self.assertEqual(updated_balance, Decimal('950'))  # Compare updated balance as Decimal

        # Test error handling (e.g., creating transaction with insufficient balance)
#        with self.assertRaises(ValueError):
#            Transaction.objects.create(
#                account=self.bank_account,
#                amount=2000,
#                balance_after_transaction=initial_balance - 2000,
#                transaction_type=1,
#                transaction_category=1
#            )

        # Test data integrity (e.g., required fields)
#        with self.assertRaises(ValueError):
#            Transaction.objects.create()

        # Test transaction history
#        transactions = Transaction.objects.filter(account=self.bank_account)
#        self.assertEqual(list(transactions), [transaction])

        # Test account balance calculation
#        self.assertEqual(self.bank_account.balance, initial_balance - 50)
