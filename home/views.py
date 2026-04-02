from django.shortcuts import render, redirect
from influencers.models import InfluencerProfile

def home(request):
    
    if request.user.is_authenticated:
        if request.user.role == 'shopkeeper':
            return redirect('shopkeepers:dashboard')
        elif request.user.role == 'influencer':
            return redirect('influencers:dashboard')

    
    influencers = InfluencerProfile.objects.all()
    category = request.GET.get('category')
    if category:
        influencers = influencers.filter(category=category)

    context = {
        'influencers': influencers
    }
    return render(request, 'home/index.html', context)