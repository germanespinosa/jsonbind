import typing
import base64
from .type_binding import TypeBinding, JsonTypes, Bindings


class BytesBinding(TypeBinding):
    def __init__(self, encoding: str):
        super().__init__(json_type=str, python_type=bytes)
        self.encoding = encoding

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        return base64.b64encode(python_value).decode(self.encoding)

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        return base64.b64decode(json_value)


Bindings.set_binding(BytesBinding(encoding='ascii'))
