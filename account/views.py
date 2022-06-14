from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm


class SignUpView(FormView):
    form_class = UserCreationForm
    template_name = 'account/signup.html'
