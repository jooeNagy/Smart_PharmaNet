import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

class ChatAPIView(APIView):
    # Public view (no authentication required)

    def post(self, request):
        user_input = request.data.get('message')

        if not user_input:
            return Response({"error": "No message provided"}, status=400)

        allowed_referers = [
            "https://smart-pharma-net.vercel.app",
            "https://127.0.0.1:8000"
        ]

        # FIXED: Changed from "http-referer" to "referer"
        request_referer = request.headers.get("referer", "")
        matched_referer = next((r for r in allowed_referers if request_referer.startswith(r)), allowed_referers[0])

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Referer": matched_referer,
            "X-Title": "Makhdoom Chat Assistant",
            "Content-Type": "application/json"  # Added this header
        }
        data = {
            "model": "openai/gpt-4o-mini",
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

            if response.status_code == 200 and "choices" in response_data:
                reply = response_data["choices"][0]["message"]["content"]
                return Response({"reply": reply})
            else:
                error_info = response_data.get("error", {})
                error_message = error_info.get("message", "Unknown error")
                error_code = error_info.get("code", response.status_code)

                return Response({
                    "error": "OpenRouter API returned an error",
                    "message": error_message,
                    "code": error_code,
                    "status_code": response.status_code,
                    "raw": response_data
                }, status=response.status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=500)