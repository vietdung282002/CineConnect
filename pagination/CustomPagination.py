from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        response = super(CustomPagination, self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        return response