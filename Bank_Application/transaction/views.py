from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required
def UserPayemnts(request):
    return render(request, 'payments.html')


@login_required
def UserDetails(request):
    return render(request, 'details.html')
