from django.db import models


class Collection(models.Model):
    added = models.DateTimeField(primary_key=True, auto_now_add=True)
    file = models.FileField()
