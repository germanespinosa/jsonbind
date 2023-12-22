from jsonbind.core.type_binding import TypeBinding, Bindings


class SetBinding(TypeBinding):
    def __init__(self):
        super().__init__(json_type=list, python_type=set)

    def to_json_value(self, python_value: set) -> list:
        return list(python_value)

    def to_python_value(self, json_value: list, python_type: type) -> set:
        return set(json_value)


Bindings.set_binding(SetBinding())
