from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField()
    slug = models.SlugField(unique=True)
