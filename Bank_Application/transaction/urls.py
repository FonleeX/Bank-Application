from django.urls import path
from .views import UserUpdateView, UserDepositView

app_name = 'transaction'


urlpatterns = [
    path('payments/', UserDepositView, name="payments" ),
    #path('details/', UserDetails, name="details" ),
    path('details/', UserUpdateView.as_view(), name="details")

]