from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import UserUpdateForm, DepositForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Transaction 
from banking.models import BankAccount

User = get_user_model()

@login_required
def UserPayemnts(request):
    return render(request, 'payments.html')


@login_required
def UserDetails(request):
    return render(request, 'details.html')

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
    

class DepositTransactionView(CreateView):
    model = Transaction
    form_class = DepositForm
    template_name = 'payments.html'
    success_url = reverse_lazy('banking:dashboard')

    def form_valid(self, form):

        transaction = form.save(commit=False)

        account = instance.account
        if account:
            account.balance += transaction.amount
            account.save()


        transaction.balance_after_transaction = account.balance
        transaction.save()

        return super().form_valid(form)


@login_required
def UserDepositView(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            account = get_object_or_404(BankAccount, user=request.user)
            if not account:
                return  HttpResponse("Error in Deposit")
            
            transaction = form.save(commit=False)
            transaction.account = account
            # Update the account balance
            account.balance += transaction.amount
            account.save()

            transaction.balance_after_transaction = account.balance
            transaction.save()
            
            return redirect('banking:dashboard')
    else:
        form = DepositForm()

    return render(request, 'payments.html', {'form': form})