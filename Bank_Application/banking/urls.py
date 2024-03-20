from django.urls import path
from .views import home, UserRegistrationView, UserLoginView, UserDashboard, UserLogout

app_name = 'banking'


urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name="register" ),
    path('login/', UserLoginView.as_view(), name="login" ),
    path('logout/', UserLogout, name='logout'),
    path('dashboard/', UserDashboard, name='dashboard'),
]