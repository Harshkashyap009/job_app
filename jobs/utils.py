# jobs/utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_application_status_email(application):
    subject = f"Your application for {application.job.title}"
    context = {
        'application': application,
        'job': application.job,
        'applicant': application.applicant.user
    }
    
    message = render_to_string('emails/application_status_update.txt', context)
    html_message = render_to_string('emails/application_status_update.html', context)
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [application.applicant.user.email],
        html_message=html_message
    )