from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинация с размером страницы 6."""

    page_size = 10  # Количество объектов на странице
    page_size_query_param = 'limit'  # Параметр запроса для изменения размера
