from django import forms 
from .models import CorporateInfo
from django.contrib.auth.models import User

class CorporateForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs = {'id':'passwordfield','class':'form-control'}),
            'email' : forms.EmailInput(attrs = {'id':'emailfield','class':'form-control'}),
            'username' : forms.TextInput(attrs = {'id':'usernamefield','class':'form-control'})
        }

class CorporateInfoForm(forms.ModelForm):
    class Meta():
        model = CorporateInfo
        fields = ['Designation','Company','picture',]
        widgets = {
            
            'Company': forms.Textarea(attrs = {'class':'form-control'}),
            'Designation' : forms.TextInput(attrs = {'class':'form-control'})
            
        }
