from django.urls import path
from userauth import views

app_name = 'userauth'

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('register/', views.register_view, name='register'),
    path('sign-in/', views.loginView, name='login'),
    path('sign-out/', views.logoutView, name='logout'),
]
