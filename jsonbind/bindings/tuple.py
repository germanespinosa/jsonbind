from jsonbind.core.type_binding import TypeBinding, Bindings


class TupleBinding(TypeBinding):
    def __init__(self):
        super().__init__(json_type=list, python_type=tuple)

    def to_json_value(self, python_value: tuple) -> list:
        return list(python_value)

    def to_python_value(self, json_value: list, python_type: type) -> tuple:
        return tuple(json_value)


Bindings.set_binding(TupleBinding())
