from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_query_param = 'p'