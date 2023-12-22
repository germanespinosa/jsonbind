import datetime
import typing
from jsonbind.core.type_binding import TypeBinding, Bindings
from enum import Enum

class DateTimeBinding(TypeBinding):
    class Format(Enum):
        time_stamp = "%Y-%m-%d %H:%M:%S.%f"
        date = "%Y-%m-%d"
        time = "%H:%M:%S.%f"
        short_time = "%H:%M:%S"
        tiny_time = "%H:%M"

    def __init__(self, date_format: typing.Union[str, "DateTimeBinding.Format"]):
        if isinstance(date_format, DateTimeBinding.Format):
            date_format = date_format.value
        super().__init__(json_type=str, python_type=datetime.datetime)
        self.date_format = date_format

    def to_json_value(self, python_value: datetime.datetime) -> str:
        return python_value.strftime(self.date_format)

    def to_python_value(self, json_value: str, python_type: type) -> datetime.datetime:
        return datetime.datetime.strptime(json_value, self.date_format)


Bindings.set_binding(DateTimeBinding(date_format=DateTimeBinding.Format.time_stamp))
