import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

class ChatAPIView(APIView):
    # Public view (no authentication required)

    def post(self, request):
        user_input = request.data.get('message')

        allowed_referers = [
            "https://smart-pharma-net.vercel.app",
            "https://127.0.0.1:8000"
        ]

        # Get referer from the request headers
        request_referer = request.headers.get("referer", "")
        matched_referer = next((r for r in allowed_referers if request_referer.startswith(r)), allowed_referers[0])

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",  # Keep it in environment, not hardcoded
            "HTTP-Referer": matched_referer,
            "X-Title": "Makhdoom Chat Assistant"
        }

        data = {
            "model": "openai/gpt-4o-mini",  # You can let users pass a model optionally
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=15
            )
            response_data = response.json()

            if "choices" in response_data:
                reply = response_data["choices"][0]["message"]["content"]
                return Response({"reply": reply})
            else:
                return Response({"error": "Unexpected response", "details": response_data}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
