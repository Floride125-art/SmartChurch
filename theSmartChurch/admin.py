from django.contrib import admin
from .models import Profile,Project, Contact
from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Item

class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass
from .models import Profile,Project, Announcements

admin.site.register(Item, MyModelAdmin)
# Register your models here.
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Announcements)
admin.site.register(Contact)

