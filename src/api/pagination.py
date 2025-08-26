from rest_framework.pagination import PageNumberPagination


class ObjectsListAPIPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page_number'
    page_size_query_param = 'page_size'
