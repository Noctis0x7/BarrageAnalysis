from django.db import models

# Create your models here.


class RawDataSet(models.Model):
    bv = models.CharField(max_length=20, primary_key=True)

    class Meta:
        db_table = 'raw_dataset'


class Barrage(models.Model):
    barrage_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255)
    bv = models.CharField(max_length=20)

    class Meta:
        db_table = 'barrage'
