import sys
import typing
import unittest

sys.path.append('..')
from jsonbind import TypeBinding, Bindings


class CustomBinding(TypeBinding):
    def __init__(self):
        super().__init__(int, str)

    def to_python_value(self, json_value: typing.Any, python_type: type) -> typing.Any:
        if json_value > 10:
            return "GREATER THAN 10"
        else:
            return "SMALLER THAN 10"

    def to_json_value(self, python_value: typing.Any) -> typing.Any:
        if python_value == "GREATER THAN 10":
            return 20
        else:
            return 0


class TypeBindingTests(unittest.TestCase):
    def test_binding(self):
        b = CustomBinding()
        self.assertEqual(b.__convert_to_json_type__("GREATER THAN 10"), 20)
        self.assertEqual(b.__convert_to_json_type__("SMALLER THAN 10"), 0)
        self.assertEqual(b.__convert_to_python_type__(5, str), "SMALLER THAN 10")
        self.assertEqual(b.__convert_to_python_type__(15, str), "GREATER THAN 10")

    def test_validations(self):
        self.assertRaises(TypeError, TypeBinding, json_type=tuple, python_type=list)
        b = TypeBinding(json_type=int, python_type=str)
        self.assertRaises(NotImplementedError, b.__convert_to_json_type__, "GREATER THAN 10")
        self.assertRaises(NotImplementedError, b.__convert_to_python_type__, 15, str)
        b = CustomBinding()
        self.assertRaises(TypeError, b.__convert_to_json_type__, 10)
        self.assertRaises(TypeError, b.__convert_to_json_type__, 20)
        self.assertRaises(TypeError, b.__convert_to_python_type__, "TEST", str)
        self.assertRaises(TypeError, b.__convert_to_python_type__, 10, int)


class BindingManagerTests(unittest.TestCase):
    def test_get_bond(self):
        bond = Bindings.get_binding(str)
        self.assertEqual(bond.to_json_value(None), None)
        self.assertEqual(bond.to_json_value(True), True)
        self.assertEqual(bond.to_json_value(10), 10)
        self.assertEqual(bond.to_json_value(1.5), 1.5)
        self.assertEqual(bond.to_json_value("Hello"), "Hello")
        self.assertEqual(bond.to_json_value([1, 2, 3]), [1, 2, 3])
        self.assertEqual(bond.to_json_value({"a": 1, "b": 2}), {"a": 1, "b": 2})
        self.assertRaises(TypeError, Bindings.get_binding, tuple)


if __name__ == '__main__':
    unittest.main()
