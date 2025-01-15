from django.db import models
from django.contrib.auth.models import User

# Profile model for user roles like 'Candidate' or 'HR'
class Profile(models.Model):
    ROLE_CHOICES = [
        ('Candidate', 'Candidate'),
        ('HR', 'HR'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

    
# Job model (remains the same)
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

# Resume model (keep it for candidate resumes)
from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume_file = models.FileField(upload_to='resumes/')
    candidate_reference = models.CharField(max_length=255, null=True, blank=True) 
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # default=1 is the ID of a default user.

    def __str__(self):
        return self.name


# RankedResume model (keep it for ranking)
class RankedResume(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.resume.name} - {self.job.title} - {self.score}"
