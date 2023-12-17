import unittest
import sys
sys.path.append('..')
from jsonbind import Serialization, Object


class A(Object):
    def __init__(self):
        super(A, self).__init__(a=10, b=20, c=30, d=[1, 2, 3], e=Object(x=20, y=30))


class BoundObjectTests(unittest.TestCase):

    def test_serialization(self):

        ti = Object(a=10, b=20, c=30)
        self.assertEqual(Serialization.serialize(ti), '{"a":10,"b":20,"c":30}')
        self.assertEqual(Serialization.serialize(A()), '{"a":10,"b":20,"c":30,"d":[1,2,3],"e":{"x":20,"y":30}}')

    def test_bytes_deserialization(self):
        self.assertEqual(Serialization.deserialize('{"a":10,"b":20,"c":30,"d":[1,2,3],"e":{"x":20,"y":30}}', A), A())


if __name__ == '__main__':
    unittest.main()
