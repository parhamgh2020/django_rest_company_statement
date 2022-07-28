from pprint import pprint
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DimCompany
from django.http import HttpResponse


@api_view(['GET'])
def search(request, *args, **kwargs):
    query  = DimCompany.objects.all()[:5]
    pprint(query)
    return Response(dict())
    # return HttpResponse('hi')