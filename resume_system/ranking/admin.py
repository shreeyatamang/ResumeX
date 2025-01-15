from django.contrib import admin
from .models import Job, Resume, RankedResume

# Registering the models to make them manageable through the Django Admin interface
admin.site.register(Job)
admin.site.register(Resume)
admin.site.register(RankedResume)
