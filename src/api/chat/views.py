import json
from django.http import JsonResponse

from api.chat.models import Message
from api.auth.views import AuthenticatedView


class PostMessageView(AuthenticatedView):
    def post(self, request):
        data = json.loads(request.body)
        # user = get_user_model().objects.get(email=email)
        user = request.user
        message = data.get('message', '')
        m = Message(message=message, user_email=user.email, author_email=user.email)
        m.save()

        automatic_response = True  # todo: tf/idf
        if automatic_response:
            response = 'stub'
            m = Message(message=response, user_email=user.email, author_email='solar_bot')
            m.save()

            return JsonResponse({
                'bot': True,
                'response': response,
            }, status=200)
        else:
            return JsonResponse({
                'bot': False,
                'message': None,
            }, status=200)


class HistoryView(AuthenticatedView):
    def get(self, request):
        shift = int(request.GET.get('shift', 0))
        count = int(request.GET.get('count', 0))

        # user = get_user_model().objects.get(email=email)
        user_messages = Message.objects.filter(user_email=request.user.email)
        messages = user_messages.order_by('-id').values()[shift:count+shift]
        return JsonResponse({
            'count': user_messages.count(),
            'content': list(messages),
        }, status=200)
