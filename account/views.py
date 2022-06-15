from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView

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
        message = render_to_string('account/email_template.html', {
            'user': user,
            'domain': get_current_site(request=self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(subject='Email Verification', message='Your Email verification Link',
                  from_email='hiahmadyan@gmail.com', recipient_list=[user.email], html_message=message)
        print('after sending')


def activate_email(request, uidb64, token):
    pass

