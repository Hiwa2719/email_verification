from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_email, name='activate-email')
]
