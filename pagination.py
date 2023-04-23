from rest_framework.pagination import PageNumberPagination


class UsersListPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_size"
    max_page_size = 100


class PostsListPagination(PageNumberPagination):
    page_size = 15
    page_query_param = "page_size"
    max_page_size = 120
