from django.urls import path
from .views import home, UserRegistrationView, UserLoginView, UserLogoutView
#from .views import home, UserRegistrationView, UserLoginView, UserDashboard

app_name = 'banking'


urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name="register" ),
    path('login/', UserLoginView.as_view(), name="login" ),
    #path('logout/', UserLogout, name='logout'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    #path('dashboard/', UserDashboard, name='dashboard'),
]