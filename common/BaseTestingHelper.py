from django.test import TestCase
from rest_framework.test import APIClient


class BaseTestingHelper(TestCase):
    client = APIClient(x_test=True)
    headers = {'x-test': True}

    def print_nice(self, test, status='----------'):
        print(f"{test: <50}\t[{status}]")
