from django import forms
from app_django.models import Admin, Employee

class LoginForm(forms.ModelForm):
    class Meta:
        model=Admin
        fields='__all__'
        labels={'username':'','password_hash':''}
        widgets={'username':forms.TextInput(attrs={'placeholder':'Enter username', 
            'autofocus':True}),
            'password_hash':forms.PasswordInput(attrs={'placeholder':'Enter password'}) }

class RegistrationForm(forms.ModelForm):
    password2=forms.CharField(label='',
            widget=forms.PasswordInput(attrs={'placeholder':'Enter password again'}) )
    class Meta:
        model=Admin
        fields='__all__'
        labels={'username':'', 'password_hash':''}
        widgets={'username':forms.TextInput(attrs={'placeholder':'Enter username',
            'autofocus':True}),
            'password_hash':forms.PasswordInput(attrs={'placeholder':'Enter password'}) }

CUSTOMER_CHOICES = [
    ('customer', 'Customer'),
    ('admin', 'Admin'),
]
class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields='__all__'
        labels={'name':'','age':'','ed':'','role':''}
        widgets={'name':forms.TextInput(attrs={'placeholder':'Enter employee name',
            'autofocus':True}),
                'age':forms.NumberInput(attrs={'placeholder':'Enter employee age'}),
                'ed':forms.TextInput(attrs={'placeholder':'Enter employee education'}),
                'role':forms.Select(choices=CUSTOMER_CHOICES)}

class DeleteEmployeeForm(forms.Form):
    id=forms.CharField(label='',
            widget=forms.NumberInput(attrs={'placeholder':'Enter employee id to be deleted',
                'autofocus':True}))

class ModifyEmployeeForm(forms.Form):
    id=forms.CharField(label='',widget=forms.NumberInput(
        attrs={'placeholder':'Enter employee id to be modified',
            'autofocus':True}))
    ed=forms.CharField(label='',required=False, widget=forms.TextInput(
        attrs={'placeholder':'Enter employee new education'}))
    role=forms.CharField(label='', required=False, widget=forms.TextInput(
        attrs={'placeholder':'Enter employee new role'}))
