from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Resume
from .serializers import ResumeSerializer
from .utils import rank_resumes  # Assuming you have this utility function
from .forms import ResumeUploadForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import UserRegisterForm

def profile(request):
    return render(request, 'profile.html')

def resume_list(request):
    resumes = Resume.objects.all()  # Fetch all resumes
    return render(request, 'resume_list.html', {'resumes': resumes})



def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home or success page
    else:
        form = ResumeUploadForm()

    return render(request, 'upload_resume.html')  # Ensure this template exists

# User Registration API for Candidates and HR
class UserRegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')  # Candidate or HR
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        user.profile.role = role  # If you want to add custom role in the profile
        user.save()
        
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# Resume Upload API
class ResumeUploadView(APIView):
    def post(self, request):
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return Response({"error": "No resume file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        resume = Resume.objects.create(
            candidate=request.user,  # Assuming the user is authenticated
            resume_file=resume_file
        )
        return Response({"message": "Resume uploaded successfully"}, status=status.HTTP_201_CREATED)

# Resume Ranking API
class ResumeRankingView(APIView):
    def post(self, request):
        job_description = request.data.get('job_description')  # You can pass the job description here
        
        # Get all resumes of candidates
        resumes = Resume.objects.all()
        
        # Ranking resumes (You will implement this function in utils.py)
        ranked_resumes = rank_resumes(job_description, resumes)
        
        return Response({"ranked_resumes": ranked_resumes}, status=status.HTTP_200_OK)

# Create a simple register view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # 'Candidate' or 'HR'
        
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role=role)
        
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    
    return render(request, 'register.html')   # This should render a form for registration

def home(request):
    return render(request, 'ranking/home.html')  # Create a `home.html` template in the `ranking/templates/ranking/` folder


def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'edit_profile.html', context)