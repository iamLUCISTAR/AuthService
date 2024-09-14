from django.urls import path
from . import views

urlpatterns = [
    # authentication api urls
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('reset-password/', views.PasswordUpdateView.as_view(), name='reset-password')
    ]