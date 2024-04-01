from django.urls import path
<<<<<<< HEAD
from .views import home, UserRegistrationView, UserLoginView, UserLogoutView
#from .views import home, UserRegistrationView, UserLoginView, UserDashboard
=======
from .views import home, UserRegistrationView, UserLoginView, UserDashboard
>>>>>>> parent of 4f2664c (Logout Function & Transaction App)

app_name = 'banking'


urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name="register" ),
    path('login/', UserLoginView.as_view(), name="login" ),
<<<<<<< HEAD
    #path('logout/', UserLogout, name='logout'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    #path('dashboard/', UserDashboard, name='dashboard'),
=======
    path('dashboard/<str:email>/', UserDashboard, name='dashboard'),
>>>>>>> parent of 4f2664c (Logout Function & Transaction App)
]