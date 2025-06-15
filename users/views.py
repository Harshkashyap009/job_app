from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import JobSeekerSignUpForm, EmployerSignUpForm

def signup(request):
    return render(request, 'users/signup.html')

def jobseeker_signup(request):
    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_jobseeker = True
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = JobSeekerSignUpForm()
    return render(request, 'users/jobseeker_signup.html', {'form': form})

def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_employer = True
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = EmployerSignUpForm()
    return render(request, 'users/employer_signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

@require_POST
def custom_logout(request):
    logout(request)
    return redirect('home')  # Redirect to your home page