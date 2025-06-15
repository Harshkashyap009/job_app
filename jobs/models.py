from django.db import models

# Create your models here.
from django.db import models
from users.models import Employer , JobSeeker
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class Job(models.Model):
    employer = models.ForeignKey('users.Employer', on_delete=models.CASCADE)
    JOB_TYPES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('RM', 'Remote'),
        ('IN', 'Internship'),
    ]
    
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=2, choices=JOB_TYPES)
    salary = models.CharField(max_length=50, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# jobs/models.py
class Application(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone = PhoneNumberField(_("phone number"), blank=True)
    email=models.EmailField(max_length=254)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=1, choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')], default='P')
    applied_date = models.DateTimeField(auto_now_add=True)
    employer_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-applied_date']
        permissions = [
            ("change_application_status", "Can change application status"),
        ]

    def __str__(self):
        return f"{self.applicant.user.username}'s application for {self.job.title}"