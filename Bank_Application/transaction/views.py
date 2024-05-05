from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import UserUpdateForm, DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Transaction 
from banking.models import BankAccount

User = get_user_model()

class UserUpdateView(TemplateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'details.html'

    def post(self, request, *args, **kwargs):
        update_form = UserUpdateForm(self.request.POST)
        if update_form.is_valid():
            user = update_form.save()
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                )   
            )
        else: 
            messages.error(request, "Error")
        return self.render_to_response(self.get_context_data(update_form=update_form))
        
    def get_context_data(self, **kwargs):
        if 'update_form' not in kwargs:
            kwargs['update_form'] = UserUpdateForm()
        return super().get_context_data(**kwargs)
    

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
    