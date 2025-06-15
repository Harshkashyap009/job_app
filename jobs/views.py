# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required# jobs/views.py
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm, ApplicationForm, ApplicationStatusForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied



def home(request):
    return render(request, 'jobs/home.html')  # Ensure this template exists

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    
    if request.user.is_jobseeker:
        has_applied = Application.objects.filter(
            job=job, 
            applicant=request.user.jobseeker
        ).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied
    })

@login_required
def post_job(request):
    if not request.user.is_employer:
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user.employer
            job.save()
            return redirect('job-detail', job_id=job.id)
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if not request.user.is_jobseeker:
        messages.error(request, 'Only job seekers can apply.')
        return redirect('jobs:job-detail', job_id=job.id)

    jobseeker = request.user.jobseeker
    already_applied = Application.objects.filter(job=job, applicant=jobseeker).exists()

    if already_applied:
        messages.info(request, 'You have already applied.')
        return render(request, 'jobs/apply_job.html', {'job': job, 'already_applied': True})

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = jobseeker
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('job-detail', job_id=job.id)
        else:
            print("Form is invalid:", form.errors)
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply_job.html', {
        'job': job,
        'form': form,
        'already_applied': False
    })

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-posted_date')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


@login_required
def employer_dashboard(request):
    if not request.user.is_employer:
        return redirect('home')
    
    jobs = Job.objects.filter(employer=request.user.employer).order_by('-posted_date')
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})

@login_required
def view_application(request, application_id):
    if not request.user.is_employer:
        return redirect('home')
    
    application = get_object_or_404(
        Application, 
        id=application_id,
        job__employer=request.user.employer
    )
    
    if request.method == 'POST':
        # Handle status updates
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES).keys():
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated')
            return redirect('jobs:view-application', application_id=application.id)
    
    return render(request, 'jobs/application_detail.html', {
        'application': application
    })
    
@login_required
def update_application(request, application_id):
    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user.employer
    )
    
    if not request.user.has_perm('jobs.change_application_status'):
        raise PermissionDenied  # This should now show no warning
    
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save()
            messages.success(request, f"Application status updated to {application.get_status_display()}")
            return redirect('jobs:view-applicants', job_id=application.job.id)
    else:
        form = ApplicationStatusForm(instance=application)
    
    return render(request, 'jobs/update_application.html', {
        'application': application,
        'form': form
    })
@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user.employer)
    applications = job.application_set.all().select_related('applicant__user')
    return render(request, 'jobs/view_applicants.html', {
        'job': job,
        'applications': applications
    })    