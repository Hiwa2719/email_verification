from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView

from .forms import SignUpFrom

User = get_user_model()


class SignUpView(FormView):
    form_class = SignUpFrom
    template_name = 'account/signup.html'

    def form_valid(self, form):
        user = form.save()
        self.send_email(user)
        return render(self.request, 'account/verification_email_send.html')

    def send_email(self, user):
        message = render_to_string('account/email_template.html', {
            'user': user,
            'domain': get_current_site(request=self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(subject='Email Verification', message='Your Email verification Link',
                  from_email='hiahmadyan@gmail.com', recipient_list=[user.email], html_message=message)


def activate_email(request, uidb64, token):
    try:
        pk = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=pk)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    if user and not user.is_active and default_token_generator.check_token(user, token):
        user.is_active = True
        return render(request, 'account/verification_success.html')
    return render(request, 'account/verification_failed.html')
