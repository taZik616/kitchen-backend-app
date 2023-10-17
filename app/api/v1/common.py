from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = 'pageSize'
    max_page_size = 120

    def get_paginated_response(self, *args, **kwargs):
        response = super().get_paginated_response(
            *args, **kwargs)
        response.data['totalPages'] = self.page.paginator.num_pages
        return response

    # Я так обнаружил что эту схему я не могу переопределить через `@extend_schema`
    # и то что эта схема подставляется в запросах ListAPIView, что заставило меня более
    # правильно использовать пагинацию теперь😹
    def get_paginated_response_schema(self, *args, **kwargs):
        schema = super().get_paginated_response_schema(
            *args, **kwargs)
        schema['properties']['totalPages'] = {
            'type': 'integer',
            'example': 123,
        }
        return schema
