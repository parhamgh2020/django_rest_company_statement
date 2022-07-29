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
    item_id = models.IntegerField()
    item_value = models.IntegerField()
    unit = models.CharField(max_length=255)
    company = models.ForeignKey(DimCompany, models.PROTECT)
    period = models.SmallIntegerField()
    period_end_to_date = models.CharField(max_length=20)

    def year(self):
        date_field: str = self.period_end_to_date
        return int(date_field.split("-")[0])
    
    def month(self):
        date_field: str = self.period_end_to_date
        return int(date_field.split("-")[1])

    class Meta:
        db_table = 'fact_statement'
