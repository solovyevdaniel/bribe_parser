from django.db import models


class Article(models.Model):
    newspaper = models.CharField(max_length=15)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    pub_date = models.DateTimeField()


class Bribe(models.Model):
    place = models.CharField(max_length=30, blank=True, null=True)
    money = models.CharField(max_length=30, blank=True, null=True)
    currency = models.CharField(max_length=30, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)