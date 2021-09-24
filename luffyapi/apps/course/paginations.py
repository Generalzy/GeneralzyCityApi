from rest_framework.pagination import PageNumberPagination as DRFPageNumberPagination


class PageNumberPagination(DRFPageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 10
