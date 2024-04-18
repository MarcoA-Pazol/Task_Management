from django import forms

#Ask for help formulary
class AskForHelp(forms.Form):
    pass

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    department = forms.CharField(max_length=200, min_length=5)
    username = forms.CharField(max_length=20, min_length=3)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)