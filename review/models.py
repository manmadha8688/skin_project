from django.db import models

# Create your models here.
class reviews(models.Model):
    ratting = models.IntegerField()
    discription = models.TextField()
    by = models.CharField()

    