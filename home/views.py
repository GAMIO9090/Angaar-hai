from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from influencers.models import InfluencerProfile
from google import genai
import json
import time




def call_gemini_with_retry(client, prompt, retries=3):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text if hasattr(response, "text") else "No response"

        except Exception as e:
            err = str(e)
            is_retryable = any(
                code in err for code in ["503", "500", "UNAVAILABLE", "overloaded"]
            )
            if is_retryable and attempt < retries - 1:
                time.sleep(2 ** attempt)   
                continue
            raise   




@csrf_exempt
def ai_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Sirf POST request allowed hai"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        language     = data.get("language", "Hinglish")
        name         = data.get("name", "User")

        if not user_message:
            return JsonResponse({"error": "Message empty hai"}, status=400)

        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        lang_instruction = {
            "Hindi":    "Sirf Hindi mein jawab do.",
            "English":  "Reply only in English.",
            "Hinglish": "Hinglish mein jawab do (Hindi + English mix).",
        }.get(language, "Hinglish mein jawab do.")

        prompt = (
            f"Tum InfluConnect platform ka helpful AI assistant ho. "
            f"{lang_instruction} "
            f"User ka naam {name} hai. "
            f"Sirf influencer marketing, bookings, platform features, "
            f"aur local business promotion se related sawaalon ka jawab do. "
            f"Agar sawaal off-topic ho toh politely redirect karo. "
            f"User ka sawaal: {user_message}"
        )

        reply = call_gemini_with_retry(client, prompt)
        return JsonResponse({"reply": reply})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        err = str(e)
        print(f"[AI Chat ERROR] {err}")

        if "429" in err:
            return JsonResponse({
                "reply": "⚠️ Thoda wait karo, API limit hit ho gayi hai. 1 minute baad try karo!"
            })

        if any(code in err for code in ["503", "UNAVAILABLE", "overloaded"]):
            return JsonResponse({
                "reply": "⚠️ AI service abhi busy hai. Thodi der baad dobara try karo 🙏"
            })

       
        return JsonResponse({
            "reply": "⚠️ Kuch galat ho gaya. Please thodi der baad try karo."
        })




def home(request):
    
    if request.user.is_authenticated:
        if hasattr(request.user, "role"):
            if request.user.role == "shopkeeper":
                return redirect("shopkeepers:shopkeeper_dashboard")
            elif request.user.role == "influencer":
                return redirect("influencers:dashboard")

    influencers = InfluencerProfile.objects.all()

    category = request.GET.get("category", "").strip()
    if category:
        influencers = influencers.filter(category=category)

    city = request.GET.get("city", "").strip()
    if city:
        influencers = influencers.filter(location__icontains=city)

    return render(request, "home/index.html", {"influencers": influencers})


def how_it_works(request):
    return render(request, "home/How it works.html")

def privacy_policy(request):
    return render(request, "home/Privacy policy.html")

def contact(request):
    return render(request, "home/Contact.html")

def terms(request):
    return render(request, "home/Terms conditions.html")