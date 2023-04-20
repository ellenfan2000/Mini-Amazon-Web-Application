from django.urls import path

from . import views
# from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('email_update',views.email_update, name='email_update'),
    path('password_update/', views.UpdatePassword.as_view(), name='password_update'),    
]
