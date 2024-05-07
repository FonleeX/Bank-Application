from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import UserEditForm, PasswordsChangeForm, DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Transaction 
from banking.models import BankAccount
from django.contrib.auth.views import PasswordChangeView
User = get_user_model()

@login_required
def UserDetails(request):
    return render(request,'details.html',{'user': request.user})

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordsChangeForm
    success_url = reverse_lazy('transaction:details')
    template_name = "change-password.html"


@login_required
def UpdateUserDetails(request):
    current_user = User.objects.get(email=request.user.email)
    form = UserEditForm(request.POST or None, instance=current_user)

    if form.is_valid():
        form.save()
        return redirect('transaction:details')

    return render(request,'change-details.html',{'user': request.user, 'form': form})
    

@login_required
def UserDeleteAccount(request):
    if request.method == 'POST':
        user = request.user
        confirm = request.POST.get("confirm_delete", False)
        if confirm:
            user.is_active = False
            user.save()
            return redirect('banking:home')
        else:
            return redirect('transaction:details')
    
    return (render(request, 'delete-user.html'))


@login_required
def UserTransactionView(request):
    account = get_object_or_404(BankAccount, user=request.user)

    deposit_form = DepositForm(account=account)
    withdrawal_form = WithdrawalForm(account=account)
    transfer_form = TransferForm(account=account)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST, account=account) 
            if deposit_form.is_valid():
                deposit_form.save()
                messages.success(request, "Deposit successful!")
                return redirect('banking:dashboard')

        elif 'withdrawal' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST, account=account)  
            if withdrawal_form.is_valid():
                withdrawal_form.save()
                messages.success(request, "Withdrawal successful!")
                return redirect('banking:dashboard')
            
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST, account=account)
            if transfer_form.is_valid():
                transfer_form.save()
                messages.success(request, "Transfer successful!")
                return redirect('banking:dashboard')
            
    return render(
        request,
        'payments.html',
        {
            'deposit_form': deposit_form,
            'withdrawal_form': withdrawal_form,
            'transfer_form': transfer_form,
        }
    )
    