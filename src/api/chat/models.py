from django.db import models


class Message(models.Model):
    user_email = models.CharField(max_length=100)
    message = models.CharField(max_length=10000)
    author_email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Message id={} email={}/>'.format(self.id, self.user_email)


class Faq(models.Model):
    question = models.CharField(max_length=10000)
    answer = models.CharField(max_length=10000)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
