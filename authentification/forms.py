from django.forms import forms, ModelForm
from django import forms
from authentification.models import CustomUser

class UserForm(ModelForm):
	class Meta:
		model = CustomUser
		fields = ['username', 'password']

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


