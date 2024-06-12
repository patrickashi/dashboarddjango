from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Student
from .models import Profile
from .models import Feedback
from .models import Payment
from .models import Notification
from .models import DiscussionBoard
from .models import Post
from .models import Comment
from .models import Result
from .models import Hostel

# Register your models here.
admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(DiscussionBoard)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Result)
admin.site.register(Hostel)

#unregister groups
admin.site.unregister(Group)