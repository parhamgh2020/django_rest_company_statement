from statistics import mode
from django.db import models


class DimCompany(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, null=True)
    state = models.SmallIntegerField()

    class Meta:
        db_table = 'dim_company'


class FactStatement(models.Model):
    item_id = models.ForeignKey('Item', on_delete=models.PROTECT)
    item_value = models.IntegerField()
    unit = models.CharField(max_length=255)
    company_id = models.ForeignKey(DimCompany, models.PROTECT)
    period = models.SmallIntegerField()
    period_end_to_date = models.DateField()

    class Meta:
        db_table = 'fact_statement'


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    no_field = models.CharField(max_length=255, default='no filed')
