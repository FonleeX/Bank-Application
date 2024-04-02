from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate ,logout
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from .forms import UserRegistrationForm
from django.http import Http404
from django.urls import reverse_lazy



User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'banking/home.html')

def redirect_to_home(request):
    return redirect('banking:home')


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
        # Assuming 'dashboard' is the name of the URL pattern for the user dashboard
        return reverse_lazy('banking:dashboard')

@login_required
def UserDashboard(request):
    return render(request, 'dashboard.html')

@login_required
def UserLogout(request):
    logout(request)
    return redirect('/')
