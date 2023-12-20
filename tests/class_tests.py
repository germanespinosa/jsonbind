import unittest
import sys
sys.path.append('..')
from jsonbind import Serialization, BoundClass


class A(BoundClass):
    def __init__(self):
        self.a = None
        self.b = True
        self.c = 10
        self.d = 10.5
        self.e = "Test"
        self.f = [1, 2, 3]
        self.g = {"x": 1, "y": 2}

    def __eq__(self, other):
        return (self.a == other.a
                and self.b == other.b
                and self.c == other.c
                and self.d == other.d
                and self.e == other.e
                and self.f == other.f
                and self.g == other.g)



class ClassBindingTests(unittest.TestCase):
    def test_class_serialization(self):
        self.assertEqual(Serialization.serialize(A()),
                         '{"a":null,"b":true,"c":10,"d":10.5,"e":"Test","f":[1,2,3],"g":{"x":1,"y":2}}')

    def test_bytes_deserialization(self):
        ti = A()
        ti.b = False
        ti.c = 20
        ti.d = 20.5
        ti.e = "Object"
        ti.f = [4, 5, 6]
        ti.g = dict({"z": 5})
        self.assertEqual(Serialization.deserialize('{"a":null,"b":false,"c": 20,"d":20.5,"e":"Object","f":[4, 5, 6],"g":{"z": 5}}', A), ti)


if __name__ == '__main__':
    unittest.main()
