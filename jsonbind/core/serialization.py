import typing
import json
from ..core.type_binding import Bindings, JsonTypes


class Serialization:

    @staticmethod
    def serialize(python_value: typing.Any, **kwargs) -> str:

        if "separators" not in kwargs:
            kwargs["separators"] = (',', ':')
        value_type = python_value.__class__
        bond = Bindings.get_binding(value_type)
        if bond:
            return json.dumps(bond.to_json_value(python_value=python_value), **kwargs)
        raise TypeError("value type '%s' is not serializable" % value_type.__name__)

    @staticmethod
    def deserialize(json_string: str,
                    python_type: type = None, **kwargs) -> typing.Any:

        json_value = json.loads(json_string, **kwargs)
        if python_type:
            bond = Bindings.get_binding(python_type=python_type)
        else:
            json_type = json_value.__class__
            bond = Bindings.get_default_binding(json_type=json_type)

        return bond.to_python_value(json_value=json_value, python_type=python_type)

    @staticmethod
    def set_default_binding(json_type: typing.Union[JsonTypes],
                            python_type: type) -> None:

        if python_type not in Bindings.bonded_python_types():
            raise TypeError("python type '%s' does not have binding")
        Serialization.__default_bonds__[json_type] = python_type


