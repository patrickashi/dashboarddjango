from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Student
from .models import Profile
from .models import Feedback

# Register your models here.
admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(Feedback)

#unregister groups
admin.site.unregister(Group)