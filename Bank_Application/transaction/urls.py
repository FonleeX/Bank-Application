from django.urls import path
from .views import UserPayemnts, UserDetails

app_name = 'transaction'


urlpatterns = [
    path('payments/', UserPayemnts, name="payments" ),
    path('details/', UserDetails, name="details" ),
]