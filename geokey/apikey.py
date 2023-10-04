from django.http import JsonResponse
# from .models import APIKey  # Adjust the import based on your project structure


class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key_header = request.headers.get('x-api-key')
        if not api_key_header:
            return JsonResponse({'error': 'API key missing'}, status=401)

        try:
            api_key = uuid.UUID(api_key_header)
            if api_key is not uuid.UUID('28d82d82-f188-4c56-97ec-fed8287d481a'):
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        except ValueError:
            return JsonResponse({'error': 'Invalid API key format'}, status=401)

        response = self.get_response(request)
        return response
