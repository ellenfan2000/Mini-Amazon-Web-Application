from django.urls import path

from . import views
# from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('email_update/',views.email_update, name='email_update'),
    path('password_update/', views.UpdatePassword.as_view(), name='password_update'),    
    path('product_details/<int:id>/',views.product_details, name='product_details'),
    path('my_orders/',views.my_orders, name='my_orders'),
    path('order_details/<int:id>/',views.order_details, name='order_details'),
    path('search_results/', views.search_results, name='search_results'),
]
