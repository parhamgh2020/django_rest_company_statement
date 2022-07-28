from pprint import pprint
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DimCompany
from django.http import HttpResponse
from django.db.models import Q
from .serializers import DimCompanySerializer


@api_view(['GET'])
def search(request, *args, **kwargs):
    name = request.query_params.get('name')
    symbol = request.query_params.get('symbol')
    company = DimCompany.objects.filter(Q(name__icontains=name) | Q(symbol__icontains=symbol))
    DimCompanySerializer(data=company)

    print('*'*50)
    print(company)
    print('*'*50)


    return Response({'name': company})
    # return HttpResponse('hi')






# @api_view(['GET'])
# def search(request, *args, **kwargs):
#     company = DimCompany.objects.get(pk=3053)
#     print('*'*50)
#     pprint(company.name)
#     print('*'*50)
#     return Response({'name': company.name})
#     # return HttpResponse('hi')
