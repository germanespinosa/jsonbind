import unittest
import sys
import enum
sys.path.append('..')
from jsonbind import Serialization, Bindings, EnumValueBinding


class TestEnum1(enum.Enum):
    value1 = 1
    value2 = 2


class TestEnum2(enum.Enum):
    value1 = 1
    value2 = 2


class TestEnum3(enum.Enum):
    value1 = True
    value2 = False


class TestEnum4(enum.Enum):
    value1 = 3.14
    value2 = 6.28


class TestEnum5(enum.Enum):
    value1 = "option1"
    value2 = "option2"


class TestEnum6(enum.Enum):
    value1 = True
    value2 = 135
    value3 = 3.14
    value4 = "option4"


class EnumTests(unittest.TestCase):
    def test_enum_serialization(self):

        self.assertEqual(Serialization.serialize(TestEnum1.value1), '"value1"')

    def test_enum_deserialization(self):
        self.assertEqual(Serialization.deserialize('"value1"', TestEnum1), TestEnum1.value1)

    def test_enum_by_value(self):
        Bindings.set_binding(EnumValueBinding(enum_type=TestEnum2))
        self.assertEqual(Serialization.serialize(TestEnum2.value1), "1")
        self.assertEqual(Serialization.serialize(TestEnum2.value2), "2")
        self.assertEqual(Serialization.deserialize("1", TestEnum2), TestEnum2.value1)
        self.assertEqual(Serialization.deserialize("2", TestEnum2), TestEnum2.value2)

        Bindings.set_binding(EnumValueBinding(enum_type=TestEnum3))
        self.assertEqual(Serialization.serialize(TestEnum3.value1), "true")
        self.assertEqual(Serialization.serialize(TestEnum3.value2), "false")
        self.assertEqual(Serialization.deserialize("true", TestEnum3), TestEnum3.value1)
        self.assertEqual(Serialization.deserialize("false", TestEnum3), TestEnum3.value2)

        Bindings.set_binding(EnumValueBinding(enum_type=TestEnum4))
        self.assertEqual(Serialization.serialize(TestEnum4.value1), "3.14")
        self.assertEqual(Serialization.serialize(TestEnum4.value2), "6.28")
        self.assertEqual(Serialization.deserialize("3.14", TestEnum4), TestEnum4.value1)
        self.assertEqual(Serialization.deserialize("6.28", TestEnum4), TestEnum4.value2)

        Bindings.set_binding(EnumValueBinding(enum_type=TestEnum5))
        self.assertEqual(Serialization.serialize(TestEnum5.value1), '"option1"')
        self.assertEqual(Serialization.serialize(TestEnum5.value2), '"option2"')
        self.assertEqual(Serialization.deserialize('"option1"', TestEnum5), TestEnum5.value1)
        self.assertEqual(Serialization.deserialize('"option2"', TestEnum5), TestEnum5.value2)

        self.assertRaises(TypeError, EnumValueBinding, enum_type=TestEnum6)


if __name__ == '__main__':
    unittest.main()
