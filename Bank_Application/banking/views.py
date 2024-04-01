from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate ,logout, login
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from .forms import UserRegistrationForm, UserAddressForm
from django.http import Http404
from django.urls import reverse_lazy



User = get_user_model()

# Create your views here.
#def home(request):
    #return render(request, 'banking/home.html')

#def redirect_to_home(request):
    #return redirect('banking:home')

class HomeView(TemplateView):
    template_name = 'banking/index.html'

class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'banking/register.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)
        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}'
                )   
            )
            return HttpResponseRedirect(reverse_lazy('transactions:deposit_money'))
        else: 
            messages.error(request, "Error")
        return self.render_to_response(self.get_context_data(registration_form=registration_form, address_form=address_form))
        
    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()
        return super().get_context_data(**kwargs)

#class UserLoginView(LoginView):
    #template_name='banking/login.html'
    #redirect_authenticated_user=True
    #def get_success_url(self):
        # Assuming 'dashboard' is the name of the URL pattern for the user dashboard
        #return reverse_lazy('banking:dashboard')

#@login_required
#def UserDashboard(request):
    #return render(request, 'dashboard.html')
class UserLoginView(LoginView):
    template_name='banking/login.html'
    redirect_authenticated_user = False

#@login_required
#def UserLogout(request):
    #logout(request)
    #return redirect('/')
class UserLogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)