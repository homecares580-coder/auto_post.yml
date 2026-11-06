import requests
import json
import random

GEMINI_API_KEY = "AQ.Ab8RN6LosyHMuLzaWXGMsaceGclAW729fgV2vVzHxe8unt2TCA"
FB_PAGE_TOKEN = "EAAXziKw5yLUBSwR2ULZBIckry2eQZBT8LlQGVpzC1pNDGUsjZBuiIicUMDs515iIUQKy8Mk9UJChXOYIU7rZBB3Ul2uePB2DqHeAhHhbsHDrhi5RZBrrlOZBaHjCVTvZB7kN5vhZCP58FhJY7aYJQqIoouEPD7tGZA60ISm9heZCgNKpFGXC5qfifIMhCqxXO7Q9419qvwYsm4YB1CMFOCYL3fiSSo4q93C1wlpxPl2WDzEIlgyjIXYdmaEs0ccCajz6kfE44QnDucLJxNu001sL9GzbodmdsWoQ5oHwZDZD"

def get_quran_verse():
    verse_number = random.randint(1, 6236)
    url = f"https://api.alquran.cloud/v1/ayah/{verse_number}/editions/quran-uthmani,bn.bengali,en.yusufali"
    try:
        res = requests.get(url).json()
        if res.get('code') == 200:
            data = res['data']
            return {
                "arabic": data[0]['text'],
                "bangla": data[1]['text'],
                "english": data[2]['text'],
                "surah_en": data[0]['surah']['englishName'],
                "surah_bn": data[0]['surah']['name'],
                "ayah": data[0]['numberInSurah']
            }
    except Exception as e:
        print(f"Error: {e}")
    return None

def generate_ai_post_content(quran_data):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    if quran_data:
        prompt = (
            f"Create an inspiring Facebook post based on this Quranic Ayah:\n"
            f"Surah: {quran_data['surah_en']} ({quran_data['surah_bn']}) Ayah {quran_data['ayah']}\n"
            f"Arabic: {quran_data['arabic']}\n"
            f"Bangla: {quran_data['bangla']}\n"
            f"English: {quran_data['english']}\n\n"
            f"Include a powerful social message for the people of Magura, and end with this exact signature:\n"
            f"প্রচারক: মো. জিয়াউল হক মামুন\n"
            f"পরিচালক, হোম কেয়ার অ্যান্ড সিকিউরিটি, মাগুরা\n"
            f"মোবাইল: ০১৯২০ ৪১৯৫৮০\n"
            f"Hashtags: #Magura #Islam #Quran #ZiaulHaqMamun #Bangladesh"
        )
    else:
        prompt = "Generate an Islamic post ending with publisher 'মো. জিয়াউল হক মামুন'."

    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return "📖 আল-কোরআনের আলো\n\nপ্রচারক: মো. জিয়াউল হক মামুন\nপরিচালক, হোম কেয়ার অ্যান্ড সিকিউরিটি, মাগুরা\nমোবাইল: ০১৯২০ ৪১৯৫৮০"

def post_to_facebook_with_image(caption):
    image_url = "https://images.unsplash.com/photo-1542810634-71277d95dcbb?q=80&w=1000&auto=format&fit=crop"
    url = "https://graph.facebook.com/v27.0/me/photos"
    payload = {'url': image_url, 'caption': caption, 'access_token': FB_PAGE_TOKEN}
    response = requests.post(url, data=payload)
    return response.json()

if __name__ == "__main__":
    q_data = get_quran_verse()
    full_caption = generate_ai_post_content(q_data)
    result = post_to_facebook_with_image(full_caption)
    print(result)
