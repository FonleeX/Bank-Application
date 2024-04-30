from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from banking.models import User
from .models import Transaction , BankAccount
from django.db import transaction

class UserUpdateForm(UserCreationForm):
    birth_date = forms.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone_number',
            'city',
            'address',
            'postcode',
        ]

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'amount']
    
    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")

        if amount <= 0:
            raise forms.ValidationError("Deposit amount must be positive")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.transaction_type = 0
        account = instance.account

        if account:
            current_balance = account.balance
            instance.balance_after_transaction = current_balance + instance.amount


        if commit:
            instance.save()
        return instance








