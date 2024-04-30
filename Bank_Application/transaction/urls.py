from django.urls import path
from .views import UserPayemnts, UserDetails, UserUpdateView, DepositTransactionView

app_name = 'transaction'


urlpatterns = [
    path('payments/', DepositTransactionView.as_view(), name="payments" ),
    #path('details/', UserDetails, name="details" ),
    path('details/', UserUpdateView.as_view(), name="details")

]