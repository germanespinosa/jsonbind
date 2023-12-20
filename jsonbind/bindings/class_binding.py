import typing
from jsonbind.core.type_binding import TypeBinding, JsonTypes, Bindings


class BoundClass(object):
    def __to_json_dict__(self) -> dict:
        new_dict = dict()
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            new_dict[key] = Bindings.to_json_value(value)
        return new_dict

    @classmethod
    def __from_json_dict__(cls, values: dict) -> "BoundClass":
        new_bound_object = cls()
        for key, value in values.items():
            if key in new_bound_object.__dict__:
                bond = Bindings.get_binding(new_bound_object.__dict__[key].__class__)
                new_bound_object.__dict__[key] = bond.to_python_value(value, new_bound_object.__dict__[key].__class__)
            else:
                new_bound_object.__dict__[key] = value
        return new_bound_object

class ClassBinding(TypeBinding):

    def __init__(self):
        super().__init__(json_type=dict, python_type=BoundClass)

    def to_json_value(self, python_value: BoundClass) -> typing.Union[JsonTypes]:
        json_value = python_value.__to_json_dict__()
        return json_value

    def to_python_value(self, json_value: dict, python_type: type) -> BoundClass:
        return python_type.__from_json_dict__(values=json_value)


Bindings.set_binding(ClassBinding())