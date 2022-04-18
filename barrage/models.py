from django.db import models

# Create your models here.


class Video(models.Model):
    bv = models.CharField(max_length=30, primary_key=True)
    status = models.IntegerField()
    sentiments = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = 'video'


class Barrage(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=100)
    bv = models.CharField(max_length=30)
    sentiments = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        db_table = 'barrages'
