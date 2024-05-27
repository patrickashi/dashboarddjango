from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import custom_login
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('register_student/', views.register_student, name='register_student'),
    path('login/', custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('view-feedback/', views.user_feedback, name='view_feedback'),
    
    path('update-profile/', views.update_profile, name='update_profile'),
    
    path('make-payment/', views.payment_form, name='payment_form'),
    path('process-payment/<int:payment_id>/', views.process_payment, name='process_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failure/', views.payment_failure, name='payment_failure'),
    
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/unread/', views.unread_notifications, name='get_unread_notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('send-notification/', views.send_notification, name='send_notification'),
    
    path('notifications/unread_count/', views.get_unread_notification_count, name='unread_notification_count'),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)