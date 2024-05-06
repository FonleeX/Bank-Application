from django.urls import path
from .views import UserUpdateView, UserTransactionView

app_name = 'transaction'


urlpatterns = [
    path('payments/', UserTransactionView, name="payments" ),
    #path('details/', UserDetails, name="details" ),
    path('details/', UserUpdateView.as_view(), name="details")
]