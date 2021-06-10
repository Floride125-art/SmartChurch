from django.contrib.auth.forms import UsernameField
from django.db.models.query_utils import refs_expression
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Christians, Profile,Project
from .forms import NewProjectForm,ProfileUpdateForm,RegisterForm, AnnouncementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer, AnnouncementsSerializer
from django.shortcuts import render
import six
import datetime as DT
import dateutil.relativedelta as REL
from django.views.generic.base import TemplateView
from django.db.models import Count
import requests,json
from datetime import datetime
def index(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'index.html',{'projects':projects})

def footer(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'footer.html',{'projects':projects})
def registerBaptism(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'registerBaptism.html',{'projects':projects})
def nav(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'nav.html',{'projects':projects})
def baptism(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'baptism.html',{'projects':projects})
def donateForm(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'donateForm.html',{'projects':projects})
def sundaySchool(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'sundaySchool.html',{'projects':projects})

def bookwedding(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'book_wedding.html',{'projects':projects})

def about(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'about.html',{'projects':projects})
class give(TemplateView):
    template_name = 'give.html'

def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.RAVE_PUBLIC_KEY
        return context
def give(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'give.html',{'projects':projects})

def watch(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'watch.html',{'projects':projects})
def sermons(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'sermons.html',{'projects':projects})
def success(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'success.html',{'projects':projects})
def allUsers(request):
    projects = Project.objects.all().order_by('-date_posted')
    return render(request, 'allUsers.html',{'projects':projects})
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            form = ContactForm()
            context = {'form': form}
            return render(request, 'footer.html', context)


# def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['key'] = settings.RAVE_PUBLIC_KEY
#         return context

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username') 
            
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            
            user = User.objects.get(username=username)
            
            profile=Profile.objects.create(user=user,email=email)
            user = authenticate(username=username, password=password)
            messages.success(request ,"Account was created for "+username)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request,'registration/registration_form.html')


@login_required(login_url='/accounts/login/') 
def rate_project(request,project_id):
    project=Project.objects.get(id=project_id)
    print(project.title)
    return render(request,"project.html",{"project":project})
@login_required(login_url='/accounts/login/') 
def my_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    projects = Project.objects.filter(user=profile.user).all()
    print(profile.user)
    form=ProfileUpdateForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            form.save()
    context={
        'form':form,
        'projects':projects,
        'profile':profile,
    }
    return render(request,"myProfile.html",context=context)


@login_required(login_url='/accounts/login/') 
def profile(request,profile_id):
    profile = Profile.objects.get(id=profile_id)
    projects = Project.objects.filter(user=profile.user).all()
    print(profile.user)
    form=ProfileUpdateForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            form.save()
    context={
        'form':form,
        'projects':projects,
        'profile':profile,
    }
    return render(request,"profile.html",context=context)

@login_required(login_url='/accounts/login/')     
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
        return redirect('index')
        
    else:
        form = NewProjectForm()
    return render(request, 'newProject.html', {"form":form, "current_user":current_user})

@login_required(login_url='/accounts/login/')     
def announcement(request):
    current_user = request.user
    if request.method == 'POST':
        form =AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = current_user
            announcement.save()
        return redirect('index')
        
    else:
        form = AnnouncementForm()
    return render(request, 'announcement.html', {"form":form, "current_user":current_user})

def search_results(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Project.search(search_term)
        print(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

class ProfileList(APIView):
    def get(self, request, fromat=None):
        all_profiles =Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)


class ProjectList(APIView):
    def get(self, request, fromat=None):
        all_projects =Project.objects.all()
        serializers =ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    
def christiansR(request):

    today = DT.date.today()
    rd = REL.relativedelta(days=1, weekday=REL.SU)
    next_sunday_date = today + rd
    if request.method == 'POST':
        firstname= request.POST['first']
        lastname= request.POST['second']
        phoneNmber= request.POST['phonenumber']
        add= request.POST['address']
        email= request.POST['email']
        dateRe=next_sunday_date
        chris= Christians.objects.all().order_by('dateRe').filter(dateRe=dateRe)
        attendee=len(chris)
        if attendee<=round(15*30/100,0):

            christians=Christians.objects.create(firstname=firstname,lastname=lastname, phoneNmber=phoneNmber,add=add,email=email,dateRe=dateRe)
            christians.save();


            d = str(next_sunday_date)
            obj={
                'sender':'CALVARY',
                'phone':phoneNmber,
                'sms':'Dear '+firstname+', You will attend the service on '+d+' in the first service.'
                }
            r=requests.post('https://send.isangegroup.com/',data=json.dumps(obj))
            print('Successfully')
            return render(request,'christiansR.html',{'message': 'Successfull Registered'})
        else: 
            obj={
                'sender':'CALVARY',
                'phone':phoneNmber,
                'sms':'Dear '+firstname+', The allowed people list is full. Please try next week'
                }
            r=requests.post('https://send.isangegroup.com/',data=json.dumps(obj))
            return render(request,'christiansR.html',{'message': 'The allowed people list is full. Please try next week'})


    else:   
     return render(request,'christiansR.html',{'dateReg': next_sunday_date})

     


        