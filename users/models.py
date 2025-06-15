from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    company_info = models.TextField(blank=True)