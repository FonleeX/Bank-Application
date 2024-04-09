from django.urls import path
from .views import UserPayemnts, UserDetails, UserUpdateView

app_name = 'transaction'


urlpatterns = [
    path('payments/', UserPayemnts, name="payments" ),
    #path('details/', UserDetails, name="details" ),
    path('details/', UserUpdateView.as_view(), name="details")

]