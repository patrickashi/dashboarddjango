from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Student
from .models import Profile
from .models import Feedback
from .models import Payment
from .models import Notification

# Register your models here.
admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(Payment)
admin.site.register(Notification)

#unregister groups
admin.site.unregister(Group)