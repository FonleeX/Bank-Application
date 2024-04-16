from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from .forms import UserUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Transaction

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
