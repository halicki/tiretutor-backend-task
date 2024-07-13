import csv

from django.db import models


class Collection(models.Model):
    id = models.BigAutoField(primary_key=True)
    added = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    def get_dictionaries(self) -> list[dict]:
        with open(self.file.path) as f:
            return list(csv.DictReader(f))
