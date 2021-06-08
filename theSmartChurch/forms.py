from django import forms
from django.urls.base import clear_script_prefix
from .models import Profile, Project, Announcements
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcements
        exclude = ['user']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','email']

#class christiansR(forms.ModelForm) : 
    #class Meta:
    # model = christiansR
       # exclude =[User]      