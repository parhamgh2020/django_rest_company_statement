from inspect import trace
from math import ceil
import traceback
from pprint import pprint

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import DimCompanySerializer, FactStatementSerializer
from rest_framework.exceptions import APIException
from .manager import SearchCompany, ValidateSearchStatement, MetricStatement
from .models import FactStatement
from django_pandas.io import read_frame


@api_view(['GET'])
def search_statement(request):
    """
    search for statement
    """
    input_data = dict()
    try:
        input_data['metric'] = request.query_params.get('metric')
        input_data['year__gte'] = request.query_params.get('year__gte')
        input_data['year__lte'] = request.query_params.get('year__lte')
        input_data['period'] = request.query_params.get('period')
        input_data['company_id'] = request.query_params.get('company_id')
        input_data['page'] = request.query_params.get('page')
        input_data['size'] = request.query_params.get('size')
        input_data = ValidateSearchStatement.validate_input_data(input_data)
        df = MetricStatement.retrieve_data(input_data)
        data = df.to_dict(orient="records")
        page, size = input_data['page'], input_data['size']
        total = len(data)
        page = ceil(total / size) if page > ceil(total / size) else page
        if total:
            return Response({
                'status_code': 200,
                'data': data[(page - 1) * size: ((page - 1) * size) + size],
                'metadata': {
                    'page': page,
                    'size': size,
                    'total': total
                },
                'message': f'{total} match' if total == 1 else f'{total} matches'
            })
        else:
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
    except Exception as err:
        print(traceback.format_exc())
        raise APIException(err)


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
