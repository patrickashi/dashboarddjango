from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student
from .models import Profile
from .models import Feedback
from .models import Payment
from .models import Post, Comment
from .models import Result
from .models import Hostel

class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        


        
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'school_name', 'favorite_subject']
        


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_photo']
        

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'school_name', 'favorite_subject', 'date_of_birth', 'gender', 'marital_status', 'nationality', 'state_of_origin',
                  'lga', 'phone_number', 'email', 'address', 'profile_photo']
        
        
        
        
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
        
class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
        
        
# Disscussionforms     
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'semester', 'code', 'load', 'title', 'grade']
        
        
class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['chosen_hostel', 'chosen_floor', 'room', 'bed_space']
        widgets = {'student': forms.HiddenInput()}
