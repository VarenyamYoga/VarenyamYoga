from django import forms
from .models import ClientInfo

from django.contrib.auth.models import User

class ClientForm(forms.ModelForm):
    
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs = {'id':'passwordfield','class':'form-control'}),
            'email' : forms.EmailInput(attrs = {'id':'emailfield','class':'form-control'}),
            'username' : forms.TextInput(attrs = {'id':'usernamefield','class':'form-control'})
        }

class ClientInfoForm(forms.ModelForm):
    class Meta():
        model = ClientInfo
        fields = ['Name','DOB','BloodGroup','Height','Weight','waist','Heap','Diseases','picture']
        widgets = {
            'Name': forms.Textarea(attrs = {'class':'form-control'}),
            'DOB' : forms.TextInput(attrs = {'class':'form-control'}),
            'BloodGroup' : forms.TextInput(attrs = {'class':'form-control'}),
            'Height' : forms.TextInput(attrs = {'class':'form-control'}),
            'Weight' : forms.TextInput(attrs = {'class':'form-control'}),
            'Waist' : forms.TextInput(attrs = {'class':'form-control'}),
            'Heap' : forms.TextInput(attrs = {'class':'form-control'}),
            'Diseases' : forms.TextInput(attrs = {'class':'form-control'}),

        }