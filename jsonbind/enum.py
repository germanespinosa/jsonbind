import enum
import typing
from .type_binding import TypeBinding, JsonTypes, Bindings


class EnumBinding(TypeBinding):

    def __init__(self):
        super().__init__(json_type=str, python_type=enum.Enum)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        return python_value.name

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        return python_type[json_value]


Bindings.set_binding(EnumBinding())


class EnumValueBinding(TypeBinding):

    def __init__(self, enum_type: type):
        if not issubclass(enum_type, enum.Enum):
            raise TypeError("enum_type must be a subclass of enum.Enum")
        json_type = None
        for element in enum_type:
            if json_type is None:
                json_type = element.value.__class__
            if not isinstance(element.value, json_type):
                raise TypeError("all elements of the Enumeration must be the same type")
        super().__init__(json_type=json_type, python_type=enum_type)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        return self.json_type(python_value.value)

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        return python_type(json_value)
