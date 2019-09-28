# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Reports(models.Model):
    user_email = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return '<Message id={} email={} approved={}/>'.format(self.id, self.user_email, self.approved)
