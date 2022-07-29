from pprint import pprint
from typing import Union

from django.db.models import Q
from pandas import DataFrame, Series, concat
from pandas.core.groupby import DataFrameGroupBy
from rest_framework.exceptions import ValidationError

from .models import DimCompany, FactStatement


class ValidateSearchStatement:
    """
    validate statement utils
    """

    @staticmethod
    def validate_pagination(page, size):
        """
        validation of page and size
        """
        if page is None:
            page = 1
        if size is None:
            size = 10
        try:
            page, size = int(page), int(size)
        except Exception as err:
            raise ValidationError('page and size should be positive integer')
        if page < 1 or size < 1:
            raise ValidationError('page and size should be positive integer')
        size = 10 if size > 10 else size
        return page, size

    @staticmethod
    def validate_year(year):
        """
        validation of year__lte and year__gte
        """
        if year is None:
            return None
        try:
            year = int(year)
        except Exception as err:
            raise ValidationError('year should be positive integer')
        if year < 0:
            raise ValidationError('year should be positive integer')
        return year

    @staticmethod
    def validate_period(period: str) -> Union[list, None]:
        """
        validation od period
        """
        if period is None or period == '':
            return None
        period = list(map(str.strip, period.split(',')))
        try:
            period = list(map(int, period))
        except Exception as err:
            raise ValidationError('period should be positive integer')
        if period:
            for num in period:
                if not num < 0:
                    continue
                raise ValidationError('period should be positive integer')
        return period

    @staticmethod
    def validate_company_id(id_list: str) -> Union[list, None]:
        """
        validation of company id
        """
        if id_list is None or id_list == '':
            return None
        id_list = list(map(str.strip, id_list.split(',')))
        try:
            id_list = list(map(int, id_list))
        except Exception as err:
            raise ValidationError('company_id should be positive integer')
        if id_list:
            for num in id_list:
                if not num < 0:
                    continue
                raise ValidationError('period should be positive integer')
        return id_list

    @staticmethod
    def validate_metric(metric: str):
        """
        metric validation
        """
        if metric is None:
            return None
        try:
            metric = int(metric)
        except Exception as err:
            raise ValidationError('metric should be 1 or 2 or 3')
        if metric in [1, 2, 3]:
            return metric
        raise ValidationError('metric should be 1 or 2 or 3')

    @classmethod
    def validate_input_data(cls, input_data: dict) -> dict:
        input_data['metric'] = cls.validate_metric(input_data['metric'])
        input_data['year__gte'] = cls.validate_year(input_data['year__gte'])
        input_data['year__lte'] = cls.validate_year(input_data['year__lte'])
        input_data['period'] = cls.validate_period(input_data['period'])
        input_data['company_id'] = cls.validate_company_id(input_data['company_id'])
        input_data['page'], input_data['size'] = cls.validate_pagination(
            input_data['page'], input_data['size'])
        return input_data


class MetricStatement:
    @staticmethod
    def get_metric_1(input_data: dict):
        qs = FactStatement.objects.filter(item_id=101)
        df = qs.to_dataframe(['item_id', 'item_value', 'company__id', 'period', 'period_end_to_date'])
        df['year'] = df.apply(lambda row: int(row['period_end_to_date'].split('-')[0]), axis=1)
        # year separation
        if input_data.get('year__gte'):
            df = df.loc[df['year'] >= input_data['year__gte']]
        if input_data.get('year__lte'):
            df = df.loc[df['year'] <= input_data['year__lte']]
        # period separation
        if input_data.get('company_id'):
            df = df.loc[df['company__id'].isin(input_data['company_id'])]
        # period separation
        if input_data.get('period'):
            df = df.loc[df['period'].isin(input_data['period'])]
        return df

    @staticmethod
    def get_metric_2(input_data: dict):
        qs = FactStatement.objects.filter(item_id__in=[101, 102])
        df: DataFrame = qs.to_dataframe(['item_id', 'item_value', 'company__id', 'period', 'period_end_to_date'])
        df['year'] = df.apply(lambda row: int(row['period_end_to_date'].split('-')[0]), axis=1)
        # year separation
        if input_data.get('year__gte'):
            df = df.loc[df['year'] >= input_data['year__gte']]
        if input_data.get('year__lte'):
            df = df.loc[df['year'] <= input_data['year__lte']]
        # period separation
        if input_data.get('company_id'):
            df = df.loc[df['company__id'].isin(input_data['company_id'])]
        # period separation
        if input_data.get('period'):
            df = df.loc[df['period'].isin(input_data['period'])]
        #  sum
        sf = df.groupby(['company__id', 'period', 'period_end_to_date'])['item_value'].sum()
        df = sf.reset_index(name='item_value')
        df = df.assign(item_id=[5000 for _ in range(len(df))])
        return df

    @staticmethod
    def get_metric_3(input_data: dict):
        qs = FactStatement.objects.filter(item_id__in=[101, 102])
        df: DataFrame = qs.to_dataframe(['item_id', 'item_value', 'company__id', 'period', 'period_end_to_date'])
        df['year'] = df.apply(lambda row: int(row['period_end_to_date'].split('-')[0]), axis=1)
        # year separation
        if input_data.get('year__gte'):
            df = df.loc[df['year'] >= input_data['year__gte']]
        if input_data.get('year__lte'):
            df = df.loc[df['year'] <= input_data['year__lte']]
        # period separation
        if input_data.get('company_id'):
            df = df.loc[df['company__id'].isin(input_data['company_id'])]
        # period separation
        if input_data.get('period'):
            df = df.loc[df['period'].isin(input_data['period'])]
        #  sum
        df_101: DataFrame = df.loc[df['item_id'] == 101]
        df_102: DataFrame = df.loc[df['item_id'] == 102]
        df_102['year'] += 1
        df = concat([df_101, df_102])
        sf = df.groupby(['company__id', 'period', 'year'])['item_value'].sum()
        df = sf.reset_index(name='item_value')
        df = df.assign(item_id=[6000 for _ in range(len(df))])
        return df

    @classmethod
    def retrieve_data(cls, input_data: dict):
        if input_data.get('metric') == 1:
            return cls.get_metric_1(input_data)
        elif input_data.get('metric') == 2:
            return cls.get_metric_2(input_data)
        elif input_data.get('metric') == 3:
            return cls.get_metric_3(input_data)


class SearchCompany:
    """
    search company utils
    """

    @staticmethod
    def validate_pagination(page, size):
        """
        validation of page and size
        """
        if page is None or page == '':
            page = 1
        if size is None or size == '':
            size = 10
        try:
            page, size = int(page), int(size)
        except Exception as err:
            raise ValidationError('page and size should be positive integer')
        if page < 1 or size < 1:
            raise ValidationError('page and size should be positive integer')
        size = 10 if size > 10 else size
        return page, size

    @staticmethod
    def get_queryset(name: str, symbol: str):
        """
        get queryset and total
        """
        if name and symbol:
            name, symbol = name.strip(), symbol.strip()
            queryset = DimCompany.objects.filter(
                Q(name__icontains=name) | Q(symbol__icontains=symbol))
        elif name:
            name.strip()
            queryset = DimCompany.objects.filter(name__icontains=name)
        elif symbol:
            symbol.strip()
            queryset = DimCompany.objects.filter(symbol__icontains=symbol)
        else:
            queryset = DimCompany.objects.all()
        return queryset, queryset.count()
