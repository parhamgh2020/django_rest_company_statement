from math import ceil
from multiprocessing import context
from pprint import pprint
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DimCompany
from django.http import HttpResponse
from django.db.models import Q
from .serializers import DimCompanySerializer
from rest_framework.exceptions import ValidationError, APIException


@api_view(['GET'])
def search(request):
    """
    search by name or symbol or both on dim_comapany table
    """
    try:
        # param
        name = request.query_params.get('name')
        symbol = request.query_params.get('symbol')
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        page, size = validate_pagination(page, size)
        #  query
        queryset, total = get_queryset(name, symbol)
        if not total:
            return Response({
                'status_code': 200,
                'data': list(),
                'metadata': {
                    'page': 0,
                    'size': 0,
                    'total': 0
                },
                'message': 'no match'
            })
        page = ceil(total / size) if page > ceil(total / size) else page
        queryset = queryset[(page - 1) * size: ((page - 1) * size) + size]
        serializer = DimCompanySerializer(
            queryset, many=True, context={'request': request})
        # result
        return Response({
            'status_code': 200,
            'data': serializer.data,
            'metadata': {
                'page': page,
                'size': size,
                'total': total
            },
            'maessage': f'{total} match' if total == 1 else f'{total} matches'
        })
    except Exception as err:
        APIException(err)


def validate_pagination(page, size):
    """
    validationo of page and size 
    """
    try:
        page, size = int(page), int(size)
    except Exception as err:
        raise ValidationError('page and size should be positive integer')
    if page < 1 or size < 1:
        raise ValidationError('page and size should be positive integer')
    size = 10 if size > 10 else size
    return page, size


def get_queryset(name: str, symbol: str):
    """
    get queryset and total
    """
    if name and symbol:
        name, symbol= name.strip(), symbol.strip()
        queryset = DimCompany.objects.filter(
            Q(name__icontains=name) | Q(symbol__icontains=symbol))
    elif name:
        name.strip()
        queryset = DimCompany.objects.filter(name__icontains=name)
    elif symbol:
        symbol.strip()
        queryset = DimCompany.objects.filter(symbol__icontains=symbol)
    else:
        raise ValidationError(
            'at least one of name and symbol fields should be filled')
    return queryset, queryset.count()
