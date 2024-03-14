from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request, 'banking/home.html')

def redirect_to_home(request):
    return redirect('home')

def register(request):
    return render(request, 'banking/register.html')

def login(request):
    return render(request, 'banking/login.html')