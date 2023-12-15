import sys
sys.path.append('..')
from jsonbind import JsonSerialization
import unittest
from enum import Enum

class TestEnum(Enum):
    value1 = 1
    value2 = 2

class EnumTests(unittest.TestCase):
    def test_bytes_serialization(self):
        self.assertEqual(JsonSerialization.serialize(TestEnum.value1),'"value1"')

    def test_bytes_deserialization(self):
        self.assertEqual(JsonSerialization.deserialize('value1', TestEnum),TestEnum.value1)


if __name__ == '__main__':
    unittest.main()
