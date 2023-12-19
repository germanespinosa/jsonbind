import typing
import json
from .type_binding import Bindings, JsonTypes


class Serialization:
    __default_bonds__: typing.Dict[type, type] = {python_type: python_type for python_type in JsonTypes}

    @staticmethod
    def serialize(value: typing.Any, **kwargs) -> str:
        if "separators" not in kwargs:
            kwargs["separators"] = (',', ':')
        value_type = value.__class__
        bond = Bindings.get_binding(value_type)
        if bond:
            return json.dumps(bond.to_json_value(python_value=value), **kwargs)
        raise TypeError("value type '%s' is not serializable" % value_type.__name__)

    @staticmethod
    def deserialize(json_string: str, python_type: type = None, **kwargs) -> typing.Any:
        json_value = json.loads(json_string, **kwargs)
        json_type = json_value.__class__
        if python_type is None:
            python_type = Serialization.__default_bonds__[json_type]

        bond = Bindings.get_binding(python_type)
        if bond:
            return bond.to_python_value(json_value=json_value, python_type=python_type)
        raise TypeError("value type '%s' is not deserializable" % json_type.__name__)

    @staticmethod
    def set_default_binding(json_type: typing.Union[JsonTypes], python_type: type) -> None:
        if python_type not in Bindings.bonded_python_types():
            raise TypeError("python type '%s' does not have binding")
        Serialization.__default_bonds__[json_type] = python_type


