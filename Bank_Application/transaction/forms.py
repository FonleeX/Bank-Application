from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from banking.models import User

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