# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Goods(models.Model):
    good_id = models.CharField(primary_key=True, max_length=8)
    good_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods'


class OriginComments(models.Model):
    comm_id = models.CharField(primary_key=True, max_length=20)
    content = models.CharField(max_length=1000, blank=True, null=True)
    good = models.ForeignKey(Goods, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'origin_comments'


class AnalysisComments(models.Model):
    comm_id = models.CharField(primary_key=True, max_length=20)
    content = models.CharField(max_length=1000, blank=True, null=True)
    sentiments = models.FloatField(blank=True, null=True)
    good = models.ForeignKey('Goods', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'analysis_comments'
