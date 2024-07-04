from django import forms
from .models import Employee, Team, Team_Task

"""LISTS FOR CHOICEABLE VALUES"""
OCCUPATION_CHOICES = [
    # BackEnd
    ['Back-End Developer', 'Back-End Developer'],
    ['Servers Engineer', 'Server Engineer'],
    # FrontEnd
    ['Front-End Developer', 'Front-End Developer'],
    # DevOps
    ['DevOps Developer', 'DevOps Developer'],
    ['Prompt Engineer', 'Prompt Engineer'],
    
    # Design
    ['Product Designer', 'Product Designer'],
    ['Graphic Designer', 'Graphic Designer'],
    ['UX Designer', 'UX Designer'],
    ['UI Designer', 'UI Designer'],
    ['UI/UX Designer', 'UI/UX Designer'],
    ['Web Designer', 'Web Designer'],
    
    # Project Management
    ['Project Manager', 'Project Manager'],
    ['SCRUM Master', 'SCRUM Master'],
    ['Agile Coach', 'Agile Coach'],
    
    # Quality Assurance (QA)
    ['Manual Tester', 'Manual Tester'],
    ['Automated Tester', 'Automated Tester'],
    ['Performance Tester', 'Performance Tester'],
    
    # Information Technology (IT)
    ['IT Support Specialist', 'IT Support Specialist'],
    ['Network Administrator', 'Network Administrator'],
    ['System Administrator', 'System Administrator'],
    ['Cybersecurity Specialist', 'Cybersecurity Specialist'],
    
    # Sales and Marketing
    ['Sales Specialist', 'Sales Specialist'],
    ['Marketing Specialist', 'Marketing Specialist'],
    ['Digital Marketer', 'Digital Marketer'],
    ['Content Marketer', 'Content Marketer'],
    ['SEO/SEM Specialist', 'SEO/SEM Specialist'],
    
    # Customer Support/Service
    ['Customer Support Specialist', 'Customer Support Specialist'],
    ['Technical Support Specialist', 'Technical Support Specialist'],
    ['Client Relations Specialist', 'Client Relations Specialist'],
    
    # Consultancy
    ['Business Consultant', 'Business Consultant'],
    ['IT Consultant', 'IT Consultant'],
    ['Strategy Consultant', 'Strategy Consultant'],
    ['Process Improvement Specialist', 'Process Improvement Specialist'],
    
    # Product Management
    ['Product Manager', 'Product Manager'],
    ['Product Strateist', 'Product Strategist'],
    ['Product Marketer', 'Product Marketer'],
    
    # Data
    ['Data Scientist', 'Data Scientist'],
    ['Data Engineer', 'Data Engineer'],
    ['Data Analyst', 'Data Analyst'],
    ['Database Manager', 'Database Manager'],
    ['Business Intelligence Analyst', 'Business Intelligence Analyst'],
    
    # Finance
    ['Accountant', 'Accountant'],
    ['Financial Planning Analyst', 'Financial Planning Analyst'],
    ['Billing Specialist', 'Billing Specialist'],
    
    # Operations
    ['Operations Manager', 'Operations Manager'],
    ['Supply Chain Manager', 'Supply Chain Manager'],
    ['Facilities Manager', 'Facilities Manager'],
    
    # Legal
    ['Legal Counsel', 'Legal Counsel'],
    ['Compliance Officer', 'Compliance Officer'],
    ['Contract Manager', 'Contract Manager'],
    
    # Research and Development (R&D)
    ['Innovation Specialist', 'Innovation Specialist'],
    ['Prototyping Specialist', 'Prototyping Specialist'],
    ['Researcher', 'Researcher'],
    
    # Training and Development
    ['Employee Training Specialist', 'Employee Training Specialist'],
    ['Leadership Development Specialist', 'Leadership Development Specialist'],
    ['Professional Development Specialist', 'Professional Development Specialist'],
    
    # Administration
    ['Office Administrator', 'Office Administrator'],
    ['Executive Assistant', 'Executive Assistant'],
    ['Receptionist', 'Receptionist'],
    
    # Vendor Management
    ['Supplier Relations Specialist', 'Supplier Relations Specialist'],
    ['Contract Negotiation Specialist', 'Contract Negotiation Specialist'],
    
    # Corporate Strategy
    ['Business Strategist', 'Business Strategist'],
    ['Market Research Analyst', 'Market Research Analyst'],
    ['Competitive Analyst', 'Competitive Analyst'],
    
    # Communications
    ['Internal Communications Specialist', 'Internal Communications Specialist'],
    ['Public Relations Specialist', 'Public Relations Specialist'],
    ['Corporate Communications Specialist', 'Corporate Communications Specialist'],
]


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


"""TEAM"""    
class JoinTeamForm(forms.Form):
    access_key = forms.CharField(max_length=8)
    
class EditTeamForm(forms.Form):
    name = forms.CharField(max_length=30, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
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
    
"""TASK"""
class CreateTeamTaskForm(forms.ModelForm):
    class Meta:
        model = Team_Task
        fields = ['title', 'description', 'due_date', 'assigned_employee']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        team = Team.objects.get(owner=user)
        self.fields['assigned_employee'].queryset = team.members.all()
        self.fields['assigned_employee'].widget.attrs.update({
            'class': 'form-control assigned-employee',
            'id': 'assignedEmployeeField'
        })

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        assigned_employee = cleaned_data.get('assigned_employee')
        if Team_Task.objects.filter(title=title, assigned_employee=assigned_employee).exists():
            self.add_error('title', 'This Task has already been assigned to this Employee.')
        return cleaned_data