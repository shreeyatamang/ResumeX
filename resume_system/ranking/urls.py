from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('registers/', views.register, name='register'),
    
    path('', views.home, name='home'),
    # API paths for Resume Upload and Ranking
    path('api/upload-resume/', views.ResumeUploadView.as_view(), name='upload_resume_api'),
    path('api/rank-resumes/', views.ResumeRankingView.as_view(), name='rank_resumes_api'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
