from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from django.contrib import messages 
from django.contrib.auth import authenticate, login

from .models import Profile
from .models import Student
from .models import Feedback
from .models import Notification

from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, StudentProfileForm
from .forms import StudentRegistrationForm
from .forms import FeedbackForm
from .forms import StudentUpdateForm

import requests
from django.conf import settings
from django.views.generic import View

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import PaymentForm
from .models import Payment
import uuid
import logging

from django.contrib.auth.decorators import user_passes_test



 


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, StudentProfileForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
        profile_form = StudentProfileForm()
    return render(request, 'dashboard/register.html', {
        'form': form,
        'profile_form': profile_form
    })



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')  # Correct field name for password
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard page
            else:
                form.add_error(None, 'Invalid username or password.')  # Add error if authentication fails
        else:
            form.add_error(None, 'Invalid username or password.')  # Add error if form is invalid
    else:
        form = AuthenticationForm()
    return render(request, 'dashboard/login.html', {'form': form})


@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('dashboard')  # Redirect to the dashboard after submitting feedback
    else:
        form = FeedbackForm()
    return render(request, 'dashboard/submit_feedback.html', {'form': form})

@login_required
def user_feedback(request):
    user_feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/view_feedback.html', {'feedbacks': user_feedbacks})


@login_required
def dashboard(request):

    firstname = request.user.first_name
    username = request.user.username  # Get the username of the logged-in user
    try:
        student = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        student = None  # or handle this case appropriately
        
    feedbacks = Feedback.objects.all().order_by('-created_at')
        
    context = { 'username': username, 'firstname': firstname, 'student': student, 'feedbacks': feedbacks}
    return render(request, 'dashboard/dashboard.html', context)

def add_sales_data(request):
    if request.method == 'POST':
        form = SalesDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard after successful form submission
    else:
        form = SalesDataForm()
    return render(request, 'dashboard/add_sales.html', {'form': form})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))  # Redirect to the profile page
    else:
        form = StudentRegistrationForm()
    return render(request, 'dashboard/register_student.html', {'form': form})

@login_required
def profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Profile does not exist.')
        return redirect('dashboard')  # Redirect to the dashboard or another appropriate page
    
    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=request.user.student)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = StudentProfileForm(instance=request.user.student)
        
    
    
    context = {'student': student, 'profile_form': profile_form}
    return render(request, 'dashboard/profile.html', context)  # Ensure this path is correct

# @login_required
# def profile(request):
#     try:
#         student = Student.objects.get(email=request.user.email)  # Assuming user is logged in and has a profile
#         return render(request, 'dashboard/profile.html', {'student': student})
#     except Student.DoesNotExist:
#         return render(request, 'dashboard/profile_not_found.html')




@login_required
def update_profile(request):
    student_profile, created = Student.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StudentUpdateForm(instance=student_profile)
    return render(request, 'dashboard/update_profile.html', {'form': form})


def student_subject_view (request):
    favourite_subject = Student.objects.get('favourite_subject')
    return render(request, 'dashboard/profile.html', {'favourite_subject' : favourite_subject})


logger = logging.getLogger(__name__)
# payment
def payment_form(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.transaction_ref = str(uuid.uuid4())  # Generate a unique transaction reference
            payment.save()
            return redirect('process_payment', payment_id=payment.id)
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = PaymentForm()
    return render(request, 'dashboard/payment_form.html', {'form': form})

@csrf_exempt
def process_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        payment_data = {
            "tx_ref": payment.transaction_ref,
            "amount": str(payment.amount),
            "currency": "NGN",
            "redirect_url": request.build_absolute_uri('/payment-success/'),
            "payment_options": "card",
            "meta": {
                "consumer_id": payment.id,
                "consumer_mac": "92a3-912ba-1192a"
            },
            "customer": {
                "email": payment.email,
                "phonenumber": payment.phone_number,
                "name": payment.name
            },
            "customizations": {
                "title": "School Fees Payment",
                "description": payment.description,
                "logo": "https://yourlogo.com/logo.png"
            }
        }

        headers = {
            'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.post('https://api.flutterwave.com/v3/payments', json=payment_data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            payment_url = response_data.get('data', {}).get('link')
            if payment_url:
                return redirect(payment_url)
            else:
                return HttpResponse("Payment initiation failed", status=500)
        else:
            return HttpResponse(f"An error occurred: {response.text}", status=500)
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {str(e)}", status=500)

def payment_success(request):
    tx_ref = request.GET.get('tx_ref')
    try:
        payment = Payment.objects.get(transaction_ref=tx_ref)
        payment.status = 'successful'
        payment.save()
        return render(request, 'payment_success.html')
    except Payment.DoesNotExist:
        logger.error(f"Payment with transaction reference {tx_ref} does not exist")
        return HttpResponse("Payment not found", status=404)

def payment_failure(request):
    return render(request, 'payment_failure.html')


#notifications
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    unread_count = notifications.filter(read=False).count()
    context = {
        "notifications": notifications,
        "unread_count": unread_count
    }
    return render(request, "dashboard/notifications.html", context)

def unread_notifications(request):
    unread_notifications = Notification.objects.filter(read=False)
    context = {'unread_notifications': unread_notifications}
    return render(request, 'dashboard/notifications.html', context)

def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect("notifications")

def get_unread_notification_count(request):
    unread_count = Notification.objects.filter(read=False).count()
    return JsonResponse({'unread_count': unread_count})

# Only allow admin users to access this view
def admin_required(user):
    return user.is_superuser

@login_required
# @user_passes_test(is_admin)
def send_notification(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        users = User.objects.all()
        for user in users:
            Notification.objects.create(user=user, title=title, message=message)
        return redirect("notifications")

    return render(request, "dashboard/send_notification.html")