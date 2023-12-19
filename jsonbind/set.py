import typing
from .type_binding import TypeBinding, JsonTypes, Bindings


class SetBinding(TypeBinding):
    def __init__(self):
        super().__init__(json_type=list, python_type=set)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        return list(python_value)

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        return set(json_value)


Bindings.set_binding(SetBinding())
