from django import forms
from .models import Employee, OCCUPATION_CHOICES, Team

#Ask for help formulary
class AskForHelpForm(forms.Form):
    reason = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)
    occupation = forms.ChoiceField(choices=OCCUPATION_CHOICES)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'address', 'birthday', 'occupation']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])  # Using set_password to hash the password
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        user.birthday = self.cleaned_data['birthday']
        user.occupation = self.cleaned_data['occupation']
        if commit:
            user.save()
        return user

    
class JoinTeamForm(forms.Form):
    access_key = forms.CharField(max_length=8)
    
class EditTeamForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)
    access_key = forms.CharField(max_length=8)
    
class CreateTeamForm(forms.Form):
    name = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea)
    access_key = forms.CharField(max_length=8)
    
    def clean_access_key(self):
        access_key = self.cleaned_data.get('access_key')
        if Team.objects.filter(access_key=access_key).exists():
            raise forms.ValidationError('This access key is already in use. Please choose a different one.')
        return access_key