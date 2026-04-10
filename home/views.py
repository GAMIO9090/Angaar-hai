from django.shortcuts import render, redirect
from influencers.models import InfluencerProfile

def home(request):
    
    if request.user.is_authenticated:
        if request.user.role == 'shopkeeper':
            return redirect('shopkeepers:shopkeeper_dashboard')
        elif request.user.role == 'influencer':
            return redirect('influencers:dashboard')

    influencers = InfluencerProfile.objects.all()
    
    
    category = request.GET.get('category')
    if category:
        influencers = influencers.filter(category=category)

    
    city = request.GET.get('city')
    if city:
        influencers = influencers.filter(location__icontains=city)

    context = {
        'influencers': influencers
    }
    return render(request, 'home/index.html', context)

def how_it_works(request):
    return render(request, 'home/how-it-works.html')

def privacy_policy(request):
    return render(request, 'home/privacy-policy.html')

def terms_conditions(request):
    return render(request, 'home/terms-and-conditions.html')