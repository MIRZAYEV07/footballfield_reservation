from rest_framework import pagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 10000


class ReviewLimitOffsetPagionation(LimitOffsetPagination):
    default_limit = 4
    max_limit = 25
    page_size_query_param = "page_size"


class RelatedBookLimitOffsetPagionation(LimitOffsetPagination):
    default_limit = 3
    max_limit = 25
    page_size_query_param = "page_size"

