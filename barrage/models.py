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


class Results(models.Model):
    bv = models.CharField(max_length=30, primary_key=True)
    zero = models.IntegerField(default=0)
    point_one = models.IntegerField(default=0)
    point_two = models.IntegerField(default=0)
    point_three = models.IntegerField(default=0)
    point_four = models.IntegerField(default=0)
    point_five = models.IntegerField(default=0)
    point_six = models.IntegerField(default=0)
    point_seven = models.IntegerField(default=0)
    point_eight = models.IntegerField(default=0)
    point_nine = models.IntegerField(default=0)
    one = models.IntegerField(default=0)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    class Meta:
        db_table = 'analysis_results'

