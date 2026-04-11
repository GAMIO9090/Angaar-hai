from django.shortcuts import render, redirect
from influencers.models import InfluencerProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from google import genai
import json


@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            language = data.get('language', 'Hinglish')
            name = data.get('name', 'User')

            if not user_message:
                return JsonResponse({'error': 'Message empty hai'}, status=400)

            
            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            
            lang_instruction = {
                'Hindi': 'Sirf Hindi mein jawab do.',
                'English': 'Reply only in English.',
                'Hinglish': 'Hinglish mein jawab do (Hindi + English mix).',
            }.get(language, 'Hinglish mein jawab do.')

            
            prompt = (
                f"Tum InfluConnect platform ka helpful AI assistant ho. "
                f"{lang_instruction} "
                f"User ka naam {name} hai. "
                f"Sirf influencer marketing, bookings, platform features, "
                f"aur local business promotion se related sawaalon ka jawab do. "
                f"Agar sawaal off-topic ho toh politely redirect karo. "
                f"User ka sawaal: {user_message}"
            )

            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            
            reply = response.text if hasattr(response, "text") else "No response"

            return JsonResponse({'reply': reply})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            error_msg = str(e)
            print("AI ERROR:", error_msg)

            
            if "429" in error_msg:
                return JsonResponse({
                    'reply': "⚠️ Thoda wait karo 😅 limit hit ho gayi hai (1 min)."
                })

            return JsonResponse({'error': error_msg}, status=500)

    return JsonResponse({'error': 'Sirf POST request allowed hai'}, status=405)


def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'role'):
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

    return render(request, 'home/index.html', {'influencers': influencers})