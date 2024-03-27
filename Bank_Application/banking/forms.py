from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User , BankAccount, BankAccountType, UserAddress

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

class UserRegistrationForm(UserCreationForm):
    #ACCOUNT_TYPES = [
        #('personal', 'Personal Account'),
        #('business', 'Business Account'),   
    #]
    #account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all()
    )
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
            #'city',
            #'address',
            #'postcode',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            birth_date = self.cleaned_data.get('birth_date')

            BankAccount.objects.create(
                user=user,
                birth_date=birth_date,
                account_type = account_type,
                account_number = (user.id + settings.ACCOUNT_NUMBER_START_FROM),
                account_sort_code = (user.id + settings.ACCOUNT_SORT_CODE_START_FROM)
            )
        return user