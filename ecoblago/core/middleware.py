from django.http import HttpRequest
from django.utils import translation

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        language = request.COOKIES.get('lang', 'ru')
        translation.activate(language)
        response = self.get_response(request)

        return response
