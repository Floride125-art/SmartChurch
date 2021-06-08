from django import forms
from django.forms import ModelForm
from .models import Profile, Project, Announcements, Contact

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')        
        if email and password:
            user = authenticate(email=email, pasword=password)
            if not user:
                raise forms.ValidationError('This user does not exist, please <a href="/register">register</a>')
            if not user.check_password(password):
                raise forms.ValidationError('You have entered the wrong password. <a href="/forgot-password">Did you forget your password?</a>')
            if not user.is_active:
                raise forms.ValidationError('This account is not active. Please <a href="/support/contact">contact support</a>')
            return super(LoginForm, self).clean(*args, **kwargs)

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'




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