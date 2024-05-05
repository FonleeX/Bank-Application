from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from banking.models import User
from .models import Transaction , BankAccount
from django.db import transaction
from django.forms import NumberInput

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


class TransactionFilterForm(forms.Form):
    TRANSACTION_TYPE_CHOICES = (
        (None, 'All'),
        (0, 'Incoming'),
        (1, 'Outgoing')
    )

    TRANSACTION_CATEGORY_CHOICES = (
        (None, 'All'),
        (0, 'Deposit'),
        (1, 'Withdrawal'),
        (2, 'Transfer'),
        (3, 'Intrest'),
        (4, 'Loan')
    )

    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    transaction_category = forms.ChoiceField(
        choices=TRANSACTION_CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Date input with form-control
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    min_amount = forms.DecimalField(
        required=False,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})  # Number input with form-control
    )

    max_amount = forms.DecimalField(
        required=False,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )





class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',  
                'step': '0.01', 
                'min': '0.01' 
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)  # Get the BankAccount instance from the view
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")

        if amount is None or amount <= 0:
            raise forms.ValidationError("Deposit amount must be positive.")

        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.account = self.account 
        instance.transaction_type = 0
        instance.transaction_category = 0
        instance.origin_account = self.account
        instance.destination_account = self.account
        instance.balance_after_transaction = self.account.balance + instance.amount 

        if commit:
            instance.save()  # Save the transaction
            self.account.balance += instance.amount  # Update the account balance
            self.account.save()  # Save the account

        return instance
    

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',  
                'step': '0.01',
                'min': '0.01' 
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)  # Get the BankAccount instance from the view
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")

        if amount is None or amount <= 0:
            raise forms.ValidationError("Deposit amount must be positive.")
        
        if self.account.balance < amount:
            raise forms.ValidationError("Insufficient balance for this withdrawal.")

        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.account = self.account 
        instance.transaction_type = 1
        instance.transaction_category = 1
        instance.origin_account = self.account
        instance.destination_account = None
        instance.balance_after_transaction = self.account.balance - instance.amount 

        if commit:
            instance.save()  
            self.account.balance -= instance.amount 
            self.account.save()  

        return instance




class TransferForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})                         
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})                         
    )
    account_number = forms.CharField(
        max_length=8,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Account Number', 'max' : '99999999', 'min' : '10000000'})
    )
    sort_code = forms.CharField(
        max_length=6,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sort Code', 'max' : '999999', 'min' : '100000'})
    )

    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',  
                'step': '0.01', 
            })
        }

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)  # Sender's account
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")

        if amount is None or amount <= 0:
            raise forms.ValidationError("Transfer amount must be positive.")

        if self.account and self.account.balance < amount:
            raise forms.ValidationError("Insufficient balance to make this transfer.")

        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        account_number = cleaned_data.get("account_number")
        sort_code = cleaned_data.get("sort_code")


        destination_account = BankAccount.objects.filter(
            user__first_name = first_name,
            user__last_name = last_name,
            account_number = account_number,
            account_sort_code = sort_code ).first()
        
        if not destination_account:
            raise forms.ValidationError("The specified account does not exist.")
        
        cleaned_data["destination_account"] = destination_account

        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        destination_account = self.cleaned_data.get("destination_account")

        instance.account = self.account
        instance.transaction_type = 1
        instance.transaction_category = 2
        instance.origin_account = self.account
        instance.destination_account = destination_account
        instance.balance_after_transaction = self.account.balance - instance.amount

        if commit:
            instance.save()

            self.account.balance -= instance.amount
            self.account.save()

            destination_instance = Transaction(
                account = destination_account,
                transaction_type = 0,
                transaction_category = 2,
                origin_account = self.account,
                destination_account = destination_account,
                balance_after_transaction = destination_account.balance + instance.amount,
                amount=instance.amount,
            )

            destination_instance.save()

            destination_account.balance += instance.amount
            destination_account.save()

        return instance    
