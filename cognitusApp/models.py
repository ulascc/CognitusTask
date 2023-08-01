from django.db import models

class Data(models.Model):
    text = models.TextField(max_length=100)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.text
    