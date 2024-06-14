from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

import uuid
import logging

from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages 
from django.contrib.auth import authenticate, login

from .models import Profile
from .models import Student, Result
from .models import Notification
from .models import Payment
from .models import DiscussionBoard, Post, Comment
from .models import Hostel
from .models import Feedback



from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, StudentProfileForm
from .forms import StudentRegistrationForm
from .forms import FeedbackForm
from .forms import StudentUpdateForm
from .forms import PaymentForm
from .forms import PostForm, CommentForm
from .forms import ResultForm
from .forms import HostelForm

import csv


import requests
from django.conf import settings
from django.views.generic import View

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



# Create your views here.
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
# feedback
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
        student = Student.objects.get(user=request.user)
    except Profile.DoesNotExist:
        student = None  # or handle this case appropriately
        
        
    context = { 'username': username, 'firstname': firstname, 'student': student}
    return render(request, 'dashboard/dashboard.html', context)



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
@csrf_exempt
# processpayment


def initiate_payment(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Ensure user is logged in
    
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_id = str(uuid.uuid4())
            # Save the initial payment record
            payment = Payment.objects.create(
                user=request.user,
                transaction_id=transaction_id,
                amount=amount,
                status='Pending'
            )
            # Correct Opay API endpoint and payload
            url = "https://sandboxapi.opaycheckout.com/api/v1/international/payment/create"  # Verify this with Opay documentation
            payload = {
                "authoriseAmount": {
                    "currency": "NGN",  # Assuming NGN, change if needed
                    "total": int(amount * 100)  # Amount should be in kobo (or smallest currency unit)
                },
                "bankcard": {
                    "cardHolderName": "David",  # Replace with actual card holder name
                    "cardNumber": "5123450000000008",  # Replace with actual card number
                    "cvv": "100",  # Replace with actual CVV
                    "enable3DS": True,
                    "expiryMonth": "01",  # Replace with actual expiry month
                    "expiryYear": "39"  # Replace with actual expiry year
                },
                "callbackUrl": request.build_absolute_uri('/payment-callback/'),
                "country": "NG",  # Replace with actual country code
                "manualCapture": True,
                "payMethod": "BankCard",
                "product": {
                    "description": "Payment for course registration",  # Replace with actual product description
                    "name": "Course Registration"  # Replace with actual product name
                },
                "reference": transaction_id,
                "returnUrl": request.build_absolute_uri('/payment_callback/'),
                "userClientIP": request.META.get('REMOTE_ADDR'),
                "userInfo": {
                    "userEmail": request.user.email,  # User email
                    "userId": str(request.user.id),  # User ID
                    # "userMobile": request.user.profile.phone_number,  # Assuming you have phone_number in profile
                    "userName": request.user.first_name  # User first name
                }
            }
            headers = {
                "Authorization": f"Bearer {settings.OPAY_SECRET_KEY}",
                "MerchantId": settings.OPAY_MERCHANT_ID
            }
            try:
                response = requests.post(url, json=payload, headers=headers)
                logger.info(f"Opay response status code: {response.status_code}")
                logger.info(f"Opay response content: {response.content}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    logger.info(f"Opay response data: {response_data}")

                    # Check if checkoutUrl is in the response data
                    checkout_url = response_data.get('checkoutUrl')

                    if checkout_url:
                        return redirect(checkout_url)
                    print(checkout_url)
                    return render(request, 'dashboard/payment_error.html', {'message': 'No checkout URL found in Opay response.'})
                else:
                    # Log detailed error information
                    logger.error(f"Authentication failed: {response.content}")
                    return render(request, 'dashboard/payment_error.html', {'message': f'Failed to initiate payment with Opay. Authentication failed. Please check your API credentials and try again.'})
            except requests.exceptions.RequestException as e:
                logger.error(f"Request Exception occurred while initiating payment: {e}")
                return render(request, 'dashboard/payment_error.html', {'message': 'Error occurred during payment initiation. Please try again later.'})
            except Exception as e:
                logger.error(f"Exception occurred while initiating payment: {e}")
                return render(request, 'dashboard/payment_error.html', {'message': f'Exception occurred: {str(e)}'})
    else:
        form = PaymentForm()
    return render(request, 'dashboard/initiate_payment.html', {'form': form, 'student': student})


def payment_callback(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('orderId')
        status = request.POST.get('status')
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = status
        payment.save()
        if status == 'SUCCESS':
            # Handle successful payment
            pass
        elif status == 'FAILED':
            # Handle failed payment
            pass
    return render(request, 'dashboard/payment_callback.html')




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
    unread_count = Notification.objects.filter(user=request.user, read=False).count()
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




# discussionviews
def discussion_board_list(request):
    boards = DiscussionBoard.objects.all()
    return render(request, 'dashboard/discussion_board_list.html', {'boards': boards})

def discussion_board_detail(request, pk):
    board = get_object_or_404(DiscussionBoard, pk=pk)
    posts = Post.objects.filter(discussion_board=board)
    return render(request, 'dashboard/discussion_board_detail.html', {'board': board, 'posts': posts})

def post_detail(request, board_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk, discussion_board_id=board_pk)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('dashboard/post_detail', board_pk=board_pk, post_pk=post_pk)
    else:
        comment_form = CommentForm()

    return render(request, 'dashboard/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def new_post(request, board_pk):
    board = get_object_or_404(DiscussionBoard, pk=board_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.discussion_board = board
            post.save()
            return redirect('discussion_board_detail', pk=board_pk)
    else:
        form = PostForm()
    return render(request, 'dashboard/new_post.html', {'form': form})


# chat
def chat(request):
    return render(request, 'dashboard/chat.html')



def upload_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload_result')
    else:
        form = ResultForm()
    return render(request, 'dashboard/upload_result.html', {'form': form})

def student_results(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    results = Result.objects.filter(student=student)
    return render(request, 'dashboard/student_results.html', {'student': student, 'results': results})


def download_results(request, student_id):
    student = Student.objects.get(student_id=student_id)
    results = Result.objects.filter(student=student)

    # Get the first name from the associated User object
    first_name = student.user.first_name

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{first_name}_results.pdf"'

    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Title
    title = f"Results for {first_name}"
    elements.append(Paragraph(title, getSampleStyleSheet()['Title']))

    # Table data
    data = [['Semester', 'Code', 'Load', 'Title', 'Grade']]
    for result in results:
        data.append([result.semester, result.code, result.load, result.title, result.grade])

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#925FE2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build PDF document
    doc.build(elements)
    return response

def hostel_form(request):
    student = Student.objects.get(user=request.user)  # Assuming you have a way to get the current student

    if request.method == 'POST':
        form = HostelForm(request.POST)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.student = student
            hostel.save()
            return redirect('hostel')  # Redirect to a success page or any other page
    else:
        form = HostelForm()
    return render(request, 'dashboard/hostel_form.html', {'form': form})


def hostel(request):
    student = Student.objects.get(user=request.user)
    hostel = Hostel.objects.filter(student=student).first()  # Assuming each student can have only one hostel entry
    
    return render(request, 'dashboard/hostel.html', {'hostel': hostel, 'student': student})

def forms(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'dashboard/forms.html', {'student': student})