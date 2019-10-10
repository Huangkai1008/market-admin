from tortoise.queryset import QuerySet


def and_pagination(query: QuerySet, page: int = 1, size: int = 10):
    """分页"""
    pos = (page - 1) * size
    return query.limit(size).offset(pos)
