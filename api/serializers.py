from rest_framework import serializers
from .models import DimCompany, FactStatement


class DimCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = DimCompany
        fields = ('symbol', 'name', 'industry', 'state',)


class FactStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactStatement
        fields = ('item_id', 'item_value',
                  'unit', 'company_id',
                  'period', 'period_end_to_date',
                   'year', 'month')
