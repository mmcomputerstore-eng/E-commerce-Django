from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User

class UserRegisterFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']
    