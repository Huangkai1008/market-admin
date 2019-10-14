import datetime as dt
from typing import Optional

from tortoise.fields import DatetimeField as _DatetimeField


class DatetimeField(_DatetimeField):
    """auto_now/auto_now_add 替换UTC time 为local time"""

    def to_db_value(
        self, value: Optional[dt.datetime], instance
    ) -> Optional[dt.datetime]:
        if self.auto_now:
            value = dt.datetime.now()
            setattr(instance, self.model_field_name, value)
            return value
        if self.auto_now_add and getattr(instance, self.model_field_name) is None:
            value = dt.datetime.now()
            setattr(instance, self.model_field_name, value)
            return value
        return value


class ModelTimeMixin:
    """增加create_time update_time字段"""

    create_time = DatetimeField(auto_now_add=True, description='创建时间')
    update_time = DatetimeField(auto_now=True, description='上次更新时间')
