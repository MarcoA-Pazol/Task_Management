from django import forms
from .models import Employee

#Ask for help formulary
class AskForHelpForm(forms.Form):
    reason = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'address', 'birthday', 'department']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])  # Using set_password to hash the password
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        user.birthday = self.cleaned_data['birthday']
        user.department = self.cleaned_data['department']
        if commit:
            user.save()
        return user

    
class JoinTeamForm(forms.Form):
    access_code = forms.CharField(max_length=8)
