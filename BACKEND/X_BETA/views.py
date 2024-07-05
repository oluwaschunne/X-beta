from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        try:
            if User.objects.filter(username=email).exists():
                return render(request, 'signup.html', {'error': 'Email already exit'})

            user = User.objects.create_user(username=email, email=email, password=password, first_name=fname, last_name=lname)
            user.profile.phone_number = phone_number
            user.profile.save()

            return redirect('signup_success', user_id=user.id)
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'An error occurred during signup. Please try again.'})

    return render(request, 'signup.html')

def signup_success_view(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'signup_success.html', {'user': user})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})       
    return render(request, 'login.html')
