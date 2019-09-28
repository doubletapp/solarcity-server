# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from api.chat.models import Faq


class FaqAdmin(admin.ModelAdmin):
    fields = ('question', 'answer', 'published')
    list_display = ('id', 'question', 'published')


admin.site.register(Faq, FaqAdmin)
