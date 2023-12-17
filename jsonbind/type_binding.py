import types
import typing

JsonTypes = types.NoneType, bool, int, float, str, dict, list


class TypeBinding(object):
    def __init__(self, json_type: type, python_type: type):
        if json_type not in JsonTypes:
            raise TypeError("json_type must be a native json type, not {}".format(json_type.__name__))
        self.json_type: type = json_type
        self.python_type: type = python_type

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        raise NotImplementedError("to_json_type() not implemented")

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        raise NotImplementedError("to_mapped_type() not implemented")

    def __convert_to_json_type__(self, python_value: typing.Any) -> typing.Any:
        if not isinstance(python_value, self.python_type):
            raise TypeError("mapped_type_value must be and instance of {}".format(self.python_type.__name__))
        json_value = self.to_json_value(python_value=python_value)
        return json_value

    def __convert_to_python_type__(self, json_value: typing.Union[JsonTypes], python_type: typing.Any) -> typing.Any:
        if not issubclass(python_type, self.python_type):
            raise TypeError("mapped_type must inherit from {}".format(self.python_type.__name__))
        python_value = self.to_python_value(json_value=json_value, python_type=python_type)
        if not isinstance(python_value, self.python_type):
            raise TypeError("to_python_value must return a {}".format(self.python_type.__name__))
        return python_value


class Bindings(object):

    __bindings__: typing.List[TypeBinding] = list()
    __bonds__: typing.Dict[type, TypeBinding] = dict()

    @staticmethod
    def set_binding(binding: TypeBinding) -> None:
        existing_bond_index = Bindings.__find_bind_by_python_type__(binding.python_type)
        if existing_bond_index is not None:
            del Bindings.__bindings__[existing_bond_index]
        Bindings.__bonds__.clear()
        Bindings.__bindings__. append(binding)

    @staticmethod
    def get_binding(python_type: type) -> TypeBinding:
        if python_type not in Bindings.__bonds__:
            binding = Bindings.find_binding(python_type)
            if binding is None:
                raise TypeError("python_type {} does not have a defined binding".format(python_type.__name__))
            Bindings.__bonds__[python_type] = binding
        return Bindings.__bonds__[python_type]

    @staticmethod
    def is_bonded(python_type: type) -> bool:
        return Bindings.get_binding(python_type=python_type) is not None

    @staticmethod
    def find_binding(python_type: type) -> typing.Union[None, TypeBinding]:
        bases = python_type.__mro__
        for base in bases:
            for binding in Bindings.__bindings__:
                if base is binding.python_type:
                    return binding
        return None

    @staticmethod
    def __find_bind_by_python_type__(python_type: type) -> typing.Union[int, None]:
        for index, binding in enumerate(Bindings.__bindings__):
            if binding.python_type is python_type:
                return index
        return None

    @staticmethod
    def bonded_python_types() -> typing.List[type]:
        bonded_types: typing.List[type] = list()
        for binding in Bindings.__bindings__:
            bonded_types.append(binding.python_type)
        return bonded_types

    @staticmethod
    def to_json_value(python_value: typing.Any) -> typing.Union[JsonTypes]:
        bond = Bindings.get_binding(python_type=python_value.__class__)
        return bond.to_json_value(python_value)

    @staticmethod
    def to_python_value(json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        bond = Bindings.get_binding(python_type=python_type)
        return bond.to_python_value(json_value=json_value, python_type=python_type)


class BaseBinding(TypeBinding):
    def __init__(self, json_type: type, python_type: type):
        super().__init__(json_type=json_type, python_type=python_type)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        return python_value

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        return json_value


class ListBinding(BaseBinding):
    def __init__(self):
        super().__init__(json_type=list, python_type=list)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        from .serialization import Bindings
        json_value = list()
        for value in python_value:
            json_value.append(Bindings.to_json_value(value))
        return python_value

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        return json_value


class DictBinding(BaseBinding):
    def __init__(self):
        super().__init__(json_type=dict, python_type=dict)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        from .serialization import Bindings
        json_value = dict()
        for key, value in python_value.items():
            json_value[key] = Bindings.to_json_value(value)
        return python_value

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        return json_value


Bindings.set_binding(BaseBinding(python_type=types.NoneType, json_type=types.NoneType))
Bindings.set_binding(BaseBinding(python_type=bool, json_type=bool))
Bindings.set_binding(BaseBinding(python_type=int, json_type=int))
Bindings.set_binding(BaseBinding(python_type=float, json_type=float))
Bindings.set_binding(BaseBinding(python_type=str, json_type=str))
Bindings.set_binding(ListBinding())
Bindings.set_binding(DictBinding())
