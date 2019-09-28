import json
import os
import pandas as pd
from django.http import JsonResponse
from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill

from api.chat.models import Message
from api.auth.views import AuthenticatedView
from api.chat.models import Faq

FAQ_PATH = '/tmp/faq_psycho.csv'


class ChatBotPredictor:
    def __init__(self):
        self._clf = None

    def load_clf(self):
        rows = Faq.objects.filter(published=True).values_list('question',
                                                              'answer')
        df = pd.DataFrame(rows, columns=['Question', 'Answer'])
        df.to_csv(FAQ_PATH, index=False)

        self._clf = SimilarityMatchingSkill(
            data_path=FAQ_PATH,
            x_col_name='Question',
            y_col_name='Answer',
            save_load_path='./model',
            config_type='tfidf_autofaq',
            edit_dict={},
            train=True
        )

    def predict(self, message, threshold=0.7):
        if self._clf is None:
            self.load_clf()

        try:
            predictions = self._clf([message], [], [])
            for text, prob in zip(*predictions):
                if prob >= threshold:
                    return text
        except:
            return None
        return None


predictor = ChatBotPredictor()


class PostMessageView(AuthenticatedView):
    def post(self, request):
        data = json.loads(request.body)
        # user = get_user_model().objects.get(email=email)
        user = request.user
        message = data.get('message', '')
        m = Message(message=message, user_email=user.email, author_email=user.email)
        m.save()

        automatic_response = predictor.predict(message)
        if automatic_response:

            m = Message(message=automatic_response, user_email=user.email, author_email='solar_bot')
            m.save()

            return JsonResponse({
                'bot': True,
                'message': automatic_response,
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
