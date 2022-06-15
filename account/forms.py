from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpFrom(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = 'password1', 'password2'

    def order_fields(self, field_order):
        return super().order_fields(['email', 'password1', 'password2'])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('User with this email already exists')
        return email

    def save(self, commit=True):
        email = username = self.cleaned_data.get('email')
        user = User(username=username, email=email, is_active=False)
        user.set_password(self.cleaned_data.get('password1'))
        user.save()
        return user
