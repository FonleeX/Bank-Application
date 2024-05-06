from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate ,logout
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from .forms import UserRegistrationForm
from transaction.forms import TransactionFilterForm
from django.http import Http404
from django.urls import reverse_lazy
from .models import BankAccount
from transaction.models import Transaction
from django.core.paginator import Paginator
from django.http import JsonResponse



User = get_user_model()

def home(request):
    return render(request, 'banking/home.html')

def redirect_to_home(request):
    return redirect('banking:home')

@login_required
def UserLogout(request):
    logout(request)
    return redirect('/')



class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'banking/register.html'

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                )   
            )
            return HttpResponseRedirect(reverse_lazy('banking:login'))
        else: 
            messages.error(request, "Error")
        return self.render_to_response(self.get_context_data(registration_form=registration_form))
        
    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        return super().get_context_data(**kwargs)

class UserLoginView(LoginView):
    template_name='banking/login.html'
    redirect_authenticated_user=True
    def get_success_url(self):
        return reverse_lazy('banking:dashboard')

@login_required
def UserDashboard(request):
    
    filter_form = TransactionFilterForm(request.GET or None)
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')  # Order by newest

    transactions = filterTransactions(transactions, filter_form)

    paginator = Paginator(transactions, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)


    return render(request, 'dashboard.html', {
        'filter_form': filter_form,
        'user': request.user,
        'transactions': transactions,
        'page_obj': page_obj
    })


def loadMoreTransactions(request):

    page_number = int(request.GET.get("page", 2))

    filter_form = TransactionFilterForm(request.GET or None)
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')  # Order by newest

    transactions = filterTransactions(transactions, filter_form)

    paginator = Paginator(transactions, 8)
    page_obj = paginator.get_page(page_number)

    transaction_data = [
        {
            "id": t.id,
            "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S"),  # Format timestamp
            "destination_user": f"{t.destination_account.user.first_name} {t.destination_account.user.last_name}"
            if t.destination_account else "",  # Check if destination account exists
            "transaction_type_display": t.get_transaction_type_display(),  # Human-readable type
            "transaction_category_display": t.get_transaction_category_display(),  # Human-readable category
            "amount": str(t.amount),  # Convert amount to string
        }
        for t in page_obj
    ]

    return JsonResponse({
        "transactions": transaction_data,
        "has_next": page_obj.has_next(),
    })


def filterTransactions(transactions, form):

    if form.is_valid():
        transaction_type = form.cleaned_data.get("transaction_type")
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)

        transaction_category = form.cleaned_data.get("transaction_category")
        if transaction_category:
            transactions = transactions.filter(transaction_category=transaction_category)

        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        if start_date:
            transactions = transactions.filter(timestamp__gte=start_date)
        if end_date:
            transactions = transactions.filter(timestamp__lte=end_date)

        min_amount = form.cleaned_data.get("min_amount")
        max_amount = form.cleaned_data.get("max_amount")
        if min_amount is not None:
            transactions = transactions.filter(amount__gte=min_amount)
        if max_amount is not None:
            transactions = transactions.filter(amount__lte=max_amount)

    return transactions