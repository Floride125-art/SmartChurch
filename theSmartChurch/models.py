from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models import Q
from django.db import models
from embed_video.fields import EmbedVideoField

class Item(models.Model):
    video = EmbedVideoField()
class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email


# Create your models here.

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture =models.ImageField(upload_to= 'profiles/', blank=True, default='profiles/default.png')
    bio = models.CharField(max_length=500, default='No bio')
    email=models.EmailField(default='No email')
    contact = models.CharField(max_length=80)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def update_bio(cls,id, bio):
        update_profile = cls.objects.filter(id = id).update(bio = bio)
        return update_profile

    @classmethod
    def get_all_profiles(cls):
        profile = Profile.objects.all()
        return profile
    @classmethod
    def search_user(cls,user):
        return cls.objects.filter(user__username__icontains=user).all()

class Project(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', default='')
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=True)
    link = models.URLField(max_length=250)
    country = models.CharField(max_length=50)

    

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_posted']

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Project.objects.filter(Q(title__icontains=searchterm)|Q(description__icontains=searchterm)|Q(country__icontains=searchterm))
        return search
        
class Announcements(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_posted']

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Announcements.objects.filter(Q(title__icontains=searchterm)|Q(description__icontains=searchterm)|Q(country__icontains=searchterm))
        return search


class Christians(models.Model):
    firstname = models.CharField(max_length =30)
    lastname = models.CharField(max_length =30)
    phoneNmber=models.CharField(max_length =30)
    add=models.CharField(max_length =30)
    email = models.EmailField()
    dateRe = models.TextField()

    def __str__(self):
        return self.firstname
    class Meta:
        ordering = ['firstname']

    def save_christian(self):
        self.save()

    def delete_christian(self):
        self.delete()




