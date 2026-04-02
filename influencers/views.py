from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InfluencerProfileForm
from .models import InfluencerProfile


@login_required
def influencer_dashboard(request):
    return redirect('shopkeepers:dashboard')


@login_required
def edit_profile(request):
    profile, created = InfluencerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('shopkeepers:dashboard')
    else:
        form = InfluencerProfileForm(instance=profile)

    return render(request, 'influencers/edit_profile.html', {'form': form})



def influencers(request):
    data = InfluencerProfile.objects.all()
    return render(request, 'influencers/influencers.html', {'influencers': data})



def influencer_detail(request, id):
    influencer = get_object_or_404(InfluencerProfile, id=id)

    return render(request, 'influencers/detail.html', {
        'influencer': influencer
    })

def influencer_detail(request, pk):
    influencer = get_object_or_404(InfluencerProfile, pk=pk)
    return render(request, 'influencers/detail.html', {'influencer': influencer})

def influencers_list(request):
    influencers = InfluencerProfile.objects.all()
    return render(request, 'influencers/influencers.html', {
        'influencers': influencers
    })