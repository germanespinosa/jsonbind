import unittest
import sys
sys.path.append('..')
from jsonbind.core import Serialization


class SerializationTests(unittest.TestCase):

    def test_serialize(self):
        self.assertEqual(Serialization.serialize(None), "null")
        self.assertEqual(Serialization.serialize(1), "1")
        self.assertEqual(Serialization.serialize(1.3), "1.3")
        self.assertEqual(Serialization.serialize(True), "true")
        self.assertEqual(Serialization.serialize(False), "false")
        self.assertEqual(Serialization.serialize("Hello"), '"Hello"')
        self.assertEqual(Serialization.serialize({"a": 1, "b": 2}), '{"a":1,"b":2}')
        self.assertEqual(Serialization.serialize([1, 2, 2.3]), '[1,2,2.3]')

    def test_deserialize(self):
        self.assertEqual(Serialization.deserialize("null"), None)
        self.assertEqual(Serialization.deserialize("1"), 1)
        self.assertEqual(Serialization.deserialize("1.3"), 1.3)
        self.assertEqual(Serialization.deserialize("true"), True)
        self.assertEqual(Serialization.deserialize("false"), False)
        self.assertEqual(Serialization.deserialize('"Hello"'), "Hello")
        self.assertEqual(Serialization.deserialize('{"a":1,"b":2}'), {"a": 1, "b": 2})
        self.assertEqual(Serialization.deserialize('[1,2,2.3]'), [1, 2, 2.3])


if __name__ == '__main__':
    unittest.main()
