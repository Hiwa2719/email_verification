from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import SignUpFrom


class SignUpView(FormView):
    form_class = SignUpFrom
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:signup')

    def form_valid(self, form):
        form.save()
        return super(SignUpView, self).form_valid(form)
