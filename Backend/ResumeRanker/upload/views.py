from django.shortcuts import render
from .models import Upload 
from .forms import UploadForms
from django.shortcuts import get_object_or_404


# Create your views here.

def index(request):
    return render(request,'index.html')

def Upload_list(request):
    Uploads = Upload.objects.all().order_by('-created_at')
    return render(request, 'Upload_list.html',{'Uploads':Uploads})

def Upload_create(request):
    if request.method == "POST":
        form = UploadForm(request.POST,request.FILES)
        pass
    else:
        form = TweetForm()
        return render (request,'tweet_form.html',{'form':form})