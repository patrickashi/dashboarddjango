from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import custom_login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('add_sales/', views.add_sales_data, name='add_sales'),
    path('register_student/', views.register_student, name='register_student'),
    path('login/', custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('view-feedback/', views.user_feedback, name='view_feedback'),
    
    path('update-profile/', views.update_profile, name='update_profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)