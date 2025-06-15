from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobSeeker, Employer

class JobSeekerSignUpForm(UserCreationForm):
    skills = forms.CharField(max_length=500, required=False)
    resume = forms.FileField(required=False)
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_jobseeker = True
        if commit:
            user.save()
            JobSeeker.objects.create(
                user=user,
                skills=self.cleaned_data.get('skills'),
                resume=self.cleaned_data.get('resume')
            )
        return user

class EmployerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    company_info = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
            Employer.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),
                company_info=self.cleaned_data.get('company_info')
            )
        return user