import typing
from .type_binding import TypeBinding, JsonTypes, Bindings


class ClassBinding(TypeBinding):

    def __init__(self, cls: type):
        super().__init__(json_type=dict, python_type=cls)
        sample_obj = cls()
        self.__members_types__: typing.Dict[str, tuple] = {}
        for member_name in vars(sample_obj):
            if member_name.startswith('_'):
                continue
            member = getattr(sample_obj, member_name)
            member_type = member.__class__
            binding = Bindings.get_binding(member_type)
            if not binding:
                raise TypeError("no binding found for member {} of type {}".format(member_name, member_type.__name__))
            self.__members_types__[member_name] = (binding, member_type)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        json_value = dict()
        for member_name, (binding, member_type) in self.__members_types__.items():
            json_value[member_name] = binding.to_json_value(getattr(python_value, member_name))
        return json_value

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        python_value = self.python_type()
        for member_name, (binding, member_type) in self.__members_types__.items():
            if member_name in json_value:
                setattr(python_value, member_name, binding.to_python_value(json_value=json_value[member_name],
                                                                           python_type=member_type))
        return python_value
