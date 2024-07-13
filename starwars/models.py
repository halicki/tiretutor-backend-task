from django.db import models

import petl as etl


class Collection(models.Model):
    id = models.BigAutoField(primary_key=True)
    added = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    def get_data(self) -> list[dict]:
        return etl.fromcsv(self.file)
