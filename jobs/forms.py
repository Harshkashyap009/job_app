from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'job_type', 'salary']

# forms.py
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'phone', 'cover_letter', 'resume']


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'employer_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'employer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

        

        