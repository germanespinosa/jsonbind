import datetime
import typing
from .type_binding import TypeBinding, JsonTypes, Bindings


class DateTimeBinding(TypeBinding):
    def __init__(self, date_format: str):
        super().__init__(json_type=str, python_type=datetime.datetime)
        self.date_format = date_format

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        return python_value.strftime(self.date_format)

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        return datetime.datetime.strptime(json_value, self.date_format)


Bindings.set_binding(DateTimeBinding(date_format='%Y-%m-%d %H:%M:%S.%f'))
