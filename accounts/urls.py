from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('password-change/', user_views.PasswordChangeView, name='PasswordChangeView'),
    path('password-change-done/', user_views.PasswordChangeDoneView, name='PasswordChangeDoneView'),
]