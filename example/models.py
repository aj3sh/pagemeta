from turtle import mode
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blogs/')
    description = models.TextField()

    def __str__(self):
        return self.title