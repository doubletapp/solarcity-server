import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, 'path').split('/')[1] == 'api':
            try:
                authentication = request.headers['authentication'].replace('JWT', '').replace(' ', '')
                payload = jwt.decode(authentication, settings.JWT_SECRET, algorithms=['HS256'])
                user = get_user_model().objects.get(email=payload['email'])
                request.user = user
            except:
                request.user = None

        response = self.get_response(request)
        return response


class SecretAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, 'path').split('/')[1] == 'api':
            if not request.META.get('HTTP_SECRET') == settings.AUTH_SECRET:
                return HttpResponseForbidden()

        response = self.get_response(request)
        return response
