import requests
from django.conf import settings

def fetch_google_image_url(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": settings.GOOGLE_CSE_API_KEY,
        "cx": settings.GOOGLE_CSE_ID,
        "q": query,
        "searchType": "image",
        "num": 1  # Only one image is enough
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["link"]
    except Exception as e:
        print("Google CSE Error:", str(e))

    return "https://via.placeholder.com/400x300?text=No+Image"
