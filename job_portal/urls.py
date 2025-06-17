"""
URL configuration for job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from jobs.views import home
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from jobs import views as job_views
from jobs.views import home
from jobs import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Job URLs
    path('employer/dashboard/', views.employer_dashboard, name='employer-dashboard'),
    path('jobs/<int:job_id>/applicants/', views.view_applicants, name='view-applicants'),
    path('applications/<int:application_id>/', views.view_application, name='view-application'),
    path('jobs/<int:job_id>/', job_views.job_detail, name='job-detail'),
    path('jobs/', job_views.job_list, name='job-list'),
    path('jobs/post/', job_views.post_job, name='post-job'),
    path('jobs/<int:job_id>/apply/', job_views.apply_job, name='apply-job'),
    path('applications/<int:application_id>/update/', views.update_application, name='update-application'),
    path('jobs/<int:job_id>/applicants/', views.view_applicants, name='view-applicants'),
    
    
    # User URLs
    path('signup/', user_views.signup, name='signup'),
    path('signup/jobseeker/', user_views.jobseeker_signup, name='jobseeker-signup'),
    path('signup/employer/', user_views.employer_signup, name='employer-signup'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)