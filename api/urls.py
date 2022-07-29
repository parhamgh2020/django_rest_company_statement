from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.search_company, name="search_company"),
    path('statement/', views.search_statement, name="search_statement"),
]
