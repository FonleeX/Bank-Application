from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .models import User , BankAccount
from django.db import transaction

class UserRegistrationForm(UserCreationForm):
    ACCOUNT_TYPES = [
        ('personal', 'Personal Account'),
        ('business', 'Business Account'),
        
    ]
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
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
            'birth_date',
            'city',
            'address',
            'postcode',
        ]

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            
            BankAccount.objects.create(
                user=user,
                account_type = account_type,
                account_number = (user.id + settings.ACCOUNT_NUMBER_START_FROM),
                account_sort_code = (user.id + settings.ACCOUNT_SORT_CODE_START_FROM)

            )