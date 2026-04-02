from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            if user.role == 'influencer':
                return redirect('influencers:dashboard')
            else:
                return redirect('shopkeepers:shopkeeper_dashboard')  
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
                return redirect('shopkeepers:shopkeeper_dashboard')  # ✅ FIX
        else:
            error = "Invalid username or password"
            return render(request, 'accounts/login.html', {'error': error})

    return render(request, 'accounts/login.html')