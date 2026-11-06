import requests
import json
import random
from datetime import datetime

# ==========================================
# এপিআই কি ও তথ্য (API Keys & Information)
# ==========================================
GEMINI_API_KEY = "AQ.Ab8RN6LosyHMuLzaWXGMsaceGclAW729fgV2vVzHxe8unt2TCA"
FB_PAGE_TOKEN = "EAAXziKw5yLUBSwR2ULZBIckry2eQZBT8LlQGVpzC1pNDGUsjZBuiIicUMDs515iIUQKy8Mk9UJChXOYIU7rZBB3Ul2uePB2DqHeAhHhbsHDrhi5RZBrrlOZBaHjCVTvZB7kN5vhZCP58FhJY7aYJQqIoouEPD7tGZA60ISm9heZCgNKpFGXC5qfifIMhCqxXO7Q9419qvwYsm4YB1CMFOCYL3fiSSo4q93C1wlpxPl2WDzEIlgyjIXYdmaEs0ccCajz6kfE44QnDucLJxNu001sL9GzbodmdsWoQ5oHwZDZD"

def get_quran_verse():
    """আন্তর্জাতিক আল-কোরআন এপিআই থেকে পর্যায়ক্রমে আরবি, বাংলা ও ইংরেজি অনুবাদসহ আয়াত সংগ্রহ"""
    # ১ থেকে ৬২৩৬ এর মধ্যে স্বয়ংক্রিয় আয়াত ট্র্যাকিং বা এলোমেলো নির্বাচন
    verse_number = random.randint(1, 6236)
    
    # আরবি, বাংলা (জহুরুল হক) এবং ইংরেজি (ইউসুফ আলী) অনুবাদ প্রাপ্তি
    url = f"https://api.alquran.cloud/v1/ayah/{verse_number}/editions/quran-uthmani,bn.bengali,en.yusufali"
    
    try:
        res = requests.get(url).json()
        if res.get('code') == 200:
            data = res['data']
            arabic = data[0]['text']
            bangla = data[1]['text']
            english = data[2]['text']
            surah_name = data[0]['surah']['englishName']
            surah_bn = data[0]['surah']['name']
            ayah_num = data[0]['numberInSurah']
            
            return {
                "arabic": arabic,
                "bangla": bangla,
                "english": english,
                "surah_en": surah_name,
                "surah_bn": surah_bn,
                "ayah": ayah_num
            }
    except Exception as e:
        print(f"Quran API Error: {e}")
    return None

def generate_ai_post_content(quran_data):
    """জেমিনি এআই দিয়ে অত্যন্ত আকর্ষণীয় ও মাগুরা কেন্দ্রিক সোশ্যাল মিডিয়া পোস্ট তৈরি"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    if quran_data:
        prompt = (
            f"Create a highly emotional, inspiring, and professional Facebook post based on this Quranic Ayah:\n"
            f"Surah: {quran_data['surah_en']} (Ayah {quran_data['ayah']})\n"
            f"Arabic: {quran_data['arabic']}\n"
            f"Bangla Meaning: {quran_data['bangla']}\n"
            f"English Meaning: {quran_data['english']}\n\n"
            f"Structure the post perfectly:\n"
            f"1. A beautiful headline for peace and unity.\n"
            f"2. Quranic Ayah in Arabic, Bangla, and English.\n"
            f"3. A short, powerful moral lesson connecting social welfare and ethical leadership for the people of Magura (মাগুরা).\n"
            f"4. End with this exact identity signature:\n"
            f"   'প্রচারক: মো. জিয়াউল হক মামুন'\n"
            f"   'পরিচালক, হোম কেয়ার অ্যান্ড সিকিউরিটি, মাগুরা'\n"
            f"   'মোবাইল: ০১৯২০ ৪১৯৫৮০'\n"
            f"5. Add trending hashtags like #Magura #Islam #Quran #ZiaulHaqMamun #Bangladesh."
        )
    else:
        prompt = "Generate an inspiring Islamic post for Magura people with Arabic, Bangla, and English quotes, ending with publisher 'মো. জিয়াউল হক মামুন'."

    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return (
            "📖 আল-কোরআনের আলো\n\n"
            "আল্লাহ তায়ালা আমাদের হেদায়েত ও সৎ পথে চলার তৌফিক দান করুন। মাগুরা জেলার সর্বস্তরের মানুষের কল্যাণ ও অগ্রগতি কামনায়—\n\n"
            "প্রচারক: মো. জিয়াউল হক মামুন\n"
            "পরিচালক, হোম কেয়ার অ্যান্ড সিকিউরিটি, মাগুরা\n"
            "মোবাইল: ০১৯২০ ৪১৯৫৮০\n"
            "#Magura #Islam #ZiaulHaqMamun"
        )

def post_to_facebook_with_image(caption):
    """এইচডি ইসলামিক ব্যানার ইমেজের সাথে ফেসবুক পেজে স্বয়ংক্রিয়ভাবে পোস্ট"""
    image_url = "https://images.unsplash.com/photo-1542810634-71277d95dcbb?q=80&w=1000&auto=format&fit=crop"
    
    url = "https://graph.facebook.com/v27.0/me/photos"
    payload = {
        'url': image_url,
        'caption': caption,
        'access_token': FB_PAGE_TOKEN
    }
    response = requests.post(url, data=payload)
    return response.json()

if __name__ == "__main__":
    print("🤖 প্রফেশনাল ইসলামিক ও স্থানীয় বট রান হচ্ছে...")
    q_data = get_quran_verse()
    full_caption = generate_ai_post_content(q_data)
    result = post_to_facebook_with_image(full_caption)
    
    if "id" in result:
        print(f"[✓] সাফল্য! ছবিসহ ফেসবুক পেজে পোস্ট হয়ে গেছে। Post ID: {result['id']}")
    else:
        print(f"[!] পোস্ট করতে সমস্যা: {result}")
