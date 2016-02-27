from django.db import models

#TODO: add migration
#Todo Add table with bribe currency place, One-to-Many
class Article(models.Model):
    newspaper = models.CharField(max_length=15)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    pub_date = models.DateTimeField()

    bribe = models.CharField(max_length=30, blank=True, null=True)
    currency = models.CharField(max_length=30, blank=True, null=True)
    place = models.CharField(max_length=30, blank=True, null=True)
