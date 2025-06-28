import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ChatAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get('message')

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:8000",  # or your domain
            "X-Title": "Makhdoom Chat Assistant"
        }

        data = {
            "model": "openai/gpt-4o-mini",  # or try 'mistralai/mixtral-8x7b'
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for a church youth portal."},
                {"role": "user", "content": user_input}
            ]
        }

        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=15)
            res_json = res.json()
            if "choices" in res_json:
                reply = res_json["choices"][0]["message"]["content"]
                return Response({"reply": reply})
            else:
                return Response({"error": "Unexpected response", "details": res_json}, status=500)           
        except Exception as e:
            return Response({"error": str(e)}, status=500)
