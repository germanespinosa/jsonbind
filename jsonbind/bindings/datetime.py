import datetime
import typing
from jsonbind.core.type_binding import TypeBinding, Bindings
from enum import Enum


class DateTimeBinding(TypeBinding):
    class Format(Enum):
        time_stamp = "%Y-%m-%d %H:%M:%S.%f"
        http_date = "%a, %d %b %Y %H:%M:%S GMT"

    def __init__(self, date_time_format: typing.Union[str, "DateTimeBinding.Format"],
                 python_type: type = None):

        if python_type:
            if not issubclass(python_type, datetime.datetime):
                raise TypeError("python_type must inherit from datetime.datetime")
        else:
            python_type = datetime.datetime
        if isinstance(date_time_format, DateTimeBinding.Format):
            date_time_format = date_time_format.value
        super().__init__(json_type=str, python_type=python_type)
        self.date_format = date_time_format

    def to_json_value(self, python_value: datetime.datetime) -> str:
        return python_value.strftime(self.date_format)

    def to_python_value(self, json_value: str,
                        python_type: type) -> datetime.datetime:
        return datetime.datetime.strptime(json_value, self.date_format)


class DateBinding(TypeBinding):
    class Format(Enum):
        date = "%Y-%m-%d"
        http_date = "%a, %d %b %Y %H:%M:%S GMT"

    def __init__(self, date_format: typing.Union[str, "DateBinding.Format"],
                 python_type: type = None):

        if python_type:
            if not issubclass(python_type, datetime.date):
                raise TypeError("python_type must inherit from datetime.date")
        else:
            python_type = datetime.date
        if isinstance(date_format, DateBinding.Format):
            date_format = date_format.value
        super().__init__(json_type=str, python_type=python_type)
        self.date_format = date_format

    def to_json_value(self, python_value: datetime.date) -> str:
        return python_value.strftime(self.date_format)

    def to_python_value(self, json_value: str,
                        python_type: type) -> datetime.date:
        dt = datetime.datetime.strptime(json_value, self.date_format)
        return self.python_type(year=dt.year,
                                month=dt.month,
                                day=dt.day)


class TimeBinding(TypeBinding):

    class Format(Enum):
        time = "%H:%M:%S.%f"
        short_time = "%H:%M:%S"
        tiny_time = "%H:%M"

    def __init__(self, time_format: typing.Union[str, "TimeBinding.Format"],
                 python_type: type = None):

        if python_type:
            if not issubclass(python_type, datetime.time):
                raise TypeError("python_type must inherit from datetime.date")
        else:
            python_type = datetime.time
        if isinstance(time_format, TimeBinding.Format):
            time_format = time_format.value
        super().__init__(json_type=str, python_type=python_type)
        self.date_format = time_format

    def to_json_value(self, python_value: datetime.date) -> str:
        return python_value.strftime(self.date_format)

    def to_python_value(self, json_value: str,
                        python_type: type) -> datetime.date:
        dt = datetime.datetime.strptime(json_value, self.date_format)
        return self.python_type(hour=dt.hour,
                                minute=dt.minute,
                                second=dt.second,
                                microsecond=dt.microsecond,
                                tzinfo=dt.tzinfo)


Bindings.set_binding(DateTimeBinding(date_time_format=DateTimeBinding.Format.time_stamp))

Bindings.set_binding(DateBinding(date_format=DateBinding.Format.date))

Bindings.set_binding(TimeBinding(time_format=TimeBinding.Format.time))
