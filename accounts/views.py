from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignupForm


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print("POST DATA:", request.POST)
        if form.is_valid():
            user = form.save()
            print("USER ROLE:", repr(user.role))
            login(request, user)
            if user.role == 'influencer':
                return redirect('influencers:dashboard')
            else:
                return redirect('shopkeepers:shopkeeper_dashboard')
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'influencer':
                return redirect('influencers:dashboard')
            else:
                return redirect('shopkeepers:shopkeeper_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')