from django.urls import path
from .views import PasswordsChangeView, UserTransactionView, UserDetails, UpdateUserDetails, UserDeleteAccount

app_name = 'transaction'


urlpatterns = [
    path('payments/', UserTransactionView, name="payments" ),
    path('details/', UserDetails, name="details" ),
    path('change_details/', UpdateUserDetails, name="change-details"),
    path('change_password/', PasswordsChangeView.as_view(), name="change-password" ),
    path('delete_user/', UserDeleteAccount, name="delete-user")
]