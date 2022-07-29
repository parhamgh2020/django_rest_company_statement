from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class SearchCompanyTestCase(APITestCase):

    def test_1(self):
        response = self.client.get(f"{reverse('search_company')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchStatementTestCase(APITestCase):

    def test_1(self):
        response = self.client.get(reverse('search_statement'))
        self.assertEqual(response.status_code, 400)
