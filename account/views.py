from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.template.loader import get_template
from django.contrib.auth.tokens import
from .forms import SignUpFrom


class SignUpView(FormView):
    form_class = SignUpFrom
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:signup')

    def form_valid(self, form):
        user = form.save()
        self.send_email(user)
        return super(SignUpView, self).form_valid(form)

    def send_email(self, user):
        template = get_template('account/email_template.html')

        send_mail(subject='Email Verification', message='Your Email verification Link',
                  recipient_list=[user.email], html_message='')


class GenerateEmail(View):
    def get(self, request, *args, **kwargs):
        pass
