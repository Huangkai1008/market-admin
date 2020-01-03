from abc import ABCMeta

from tortoise import QuerySet

__all__ = ['BaseRepository']


class BaseRepository(metaclass=ABCMeta):
    """基础Repo"""

    @staticmethod
    def _and_pagination(query: QuerySet, page: int = 1, size: int = 10) -> QuerySet:
        """分页"""
        pos = (page - 1) * size
        return query.limit(size).offset(pos)
