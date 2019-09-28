from django.db import models


class Message(models.Model):
    user_email = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    author_email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Message id={} email={}/>'.format(self.id, self.user_email)
