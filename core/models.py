from django.db import models


class Article(models.Model):
    newspaper = models.CharField(max_length=15)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    pub_date = models.DateTimeField()
    bribe = models.CharField(max_length=30, blank=True)
    place = models.CharField(max_length=30, blank=True)
