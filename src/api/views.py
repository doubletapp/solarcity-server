# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse

from api.models import Reports
from api.auth.views import AuthenticatedView

# Create your views here.


class PostReportView(AuthenticatedView):
    def post(self, request):
        user = request.user
        r = Reports(content=request.body.decode('utf-8'), user_email=user.email)
        r.save()

        return JsonResponse({
            'status': 'OK',
        }, status=200)


class ReportsHistoryView(AuthenticatedView):
    def get(self, request):
        shift = int(request.GET.get('shift', 0))
        count = int(request.GET.get('count', 0))

        user_reports = Reports.objects.filter(user_email=request.user.email)
        reports = user_reports.order_by('-id').values()[shift:count+shift]
        return JsonResponse({
            'count': user_reports.count(),
            'content': list(reports),
        }, status=200)
