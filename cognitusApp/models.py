from django.db import models

class Data(models.Model):
    text = models.TextField(max_length=100)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.text
    

class TrainingLog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255)
