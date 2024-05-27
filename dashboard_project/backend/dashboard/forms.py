from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student
from .models import Profile
from .models import Feedback
from .models import Payment

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
        fields = ['school_name', 'favorite_subject', 'profile_photo']
        
        
        
        
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'description', 'amount', 'email', 'phone_number']
