import requests
import json
from datetime import datetime

# ==========================================
# আপনার সিক্রেট কি ও ফেসবুক পেজ টোকেন
# ==========================================
GEMINI_API_KEY = "AQ.Ab8RN6LosyHMuLzaWXGMsaceGclAW729fgV2vVzHxe8unt2TCA"
FB_PAGE_TOKEN = "EAAXziKw5yLUBSwR2ULZBIckry2eQZBT8LlQGVpzC1pNDGUsjZBuiIicUMDs515iIUQKy8Mk9UJChXOYIU7rZBB3Ul2uePB2DqHeAhHhbsHDrhi5RZBrrlOZBaHjCVTvZB7kN5vhZCP58FhJY7aYJQqIoouEPD7tGZA60ISm9heZCgNKpFGXC5qfifIMhCqxXO7Q9419qvwYsm4YB1CMFOCYL3fiSSo4q93C1wlpxPl2WDzEIlgyjIXYdmaEs0ccCajz6kfE44QnDucLJxNu001sL9GzbodmdsWoQ5oHwZDZD"

def post_to_facebook(caption):
    """মেটা গ্রাফ এপিআই দিয়ে ফেসবুক পেজে স্বয়ংক্রিয়ভাবে পোস্ট করার ফাংশন"""
    url = "https://graph.facebook.com/v27.0/me/feed"
    payload = {
        'message': caption,
        'access_token': FB_PAGE_TOKEN
    }
    response = requests.post(url, data=payload)
    return response.json()

def generate_islamic_and_local_content():
    """জেমিনি এআই দিয়ে ইসলামিক, কোরআনের আয়াত ও মাগুরা কেন্দ্রিক কন্টেন্ট তৈরি"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = (
        "Create a viral, highly engaging social media post in Bengali focusing on Islamic values, Quranic verses with meaning, "
        "Hadith, and moral teachings. It must specially connect with the people of Magura district (মাগুরা জেলা) and all over Bangladesh, "
        "promoting welfare, community development, and positivity. Add trending hashtags."
    )
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    res_json = response.json()
    
    try:
        caption = res_json['candidates'][0]['content']['parts'][0]['text']
        return caption
    except Exception as e:
        return "বিসমিল্লাহির রহমানির রাহিম। আল্লাহ আমাদের সকলের সহায় হোন। #Magura #Islam #Bangladesh"

if __name__ == "__main__":
    print("🤖 গিটহব অ্যাকশনস থেকে স্বয়ংক্রিয় পোস্ট প্রসেস শুরু হচ্ছে...")
    
    auto_caption = generate_islamic_and_local_content()
    res = post_to_facebook(auto_caption)
    
    if "id" in res:
        print(f"[✓] সফলভাবে ফেসবুক পেজে স্বয়ংক্রিয় পোস্ট হয়ে গেছে! Post ID: {res['id']}")
    else:
        print(f"[!] পোস্ট করতে গিয়ে সমস্যা হয়েছে: {res}")
