from inspect import trace
from math import ceil
import traceback
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import DimCompanySerializer, FactStatementSerializer
from rest_framework.exceptions import APIException
from .manager import SearchCompany, SearchStatement


@api_view(['GET'])
def search_company(request):
    """
    search by name or symbol or both on dim_comapany table
    """
    try:
        # param
        name = request.query_params.get('name')
        symbol = request.query_params.get('symbol')
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        page, size = SearchCompany.validate_pagination(page, size)
        #  query
        queryset, total = SearchCompany.get_queryset(name, symbol)
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
            'message': f'{total} match' if total == 1 else f'{total} matches'
        })
    except Exception as err:
        raise APIException(err)


@api_view(['GET'])
def search_statement(request):
    """
    search for statement 
    """
    try:
        metric = request.query_params.get('metric')
        year__gte = request.query_params.get('year__gte')
        year__lte = request.query_params.get('year__lte')
        period = request.query_params.get('period')
        company_id = request.query_params.get('company_id')
        queryset = SearchStatement.metric_1()
        serializers = FactStatementSerializer(
            queryset, many=True, context={'request': request})
        return Response({
            'metric': metric,
            'year__gte': year__gte,
            'year__lte': year__lte,
            'period': period,
            'company_id': company_id,
            'result': serializers.data
        })
    except Exception as err:
        print(traceback.format_exc())
        raise APIException(err)
