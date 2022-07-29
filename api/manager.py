from .models import DimCompany, FactStatement
from rest_framework.exceptions import ValidationError
from django.db.models import Q
# from django_pandas.io import read_frame


# qs = MyModel.objects.all()


class SearchStatement:
    """
    search statement utils
    """

    @staticmethod
    def metric_1():
        queryset = FactStatement.objects.all()[:10]
        return queryset
        # df = read_frame(queryset)
        # return df.head()


class SearchCompany:
    """
    search compnay utils
    """

    @staticmethod
    def validate_pagination(page, size):
        """
        validationo of page and size 
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
