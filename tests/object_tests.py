import unittest
import sys
sys.path.append('..')
from jsonbind import Serialization, Object


class A(Object):
    def __init__(self):
        super(A, self).__init__(a=10, b=20, c=30, d=[1, 2, 3], e=Object(x=20, y=30))


class B(Object):
    def __init__(self):
        super(B, self).__init__(a=None, b=True, c=30, d=18.5, e="TEST", f=[1, 2, 3], g=Object(x=20, y=30.3, z="TEST"))


class C(Object):
    def __init__(self):
        super(C, self).__init__(a=None, b=False, c=60, d=6.7, e="CONTROL", f=[9, 8, 7], g=Object(x=22, y=33.3, z="CONTROL"))


class BoundObjectTests(unittest.TestCase):

    def test_serialization(self):

        ti = Object(a=10, b=20, c=30)
        self.assertEqual(Serialization.serialize(ti), '{"a":10,"b":20,"c":30}')
        self.assertEqual(Serialization.serialize(A()), '{"a":10,"b":20,"c":30,"d":[1,2,3],"e":{"x":20,"y":30}}')
        self.assertEqual(str(A()), '{"a":10,"b":20,"c":30,"d":[1,2,3],"e":{"x":20,"y":30}}')

    def test_deserialization(self):
        self.assertEqual(Serialization.deserialize('{"a":10,"b":20,"c":30,"d":[1,2,3],"e":{"x":20,"y":30}}', A), A())
        self.assertEqual(A.parse('{"a":10,"b":20,"c":30,"d":[1,2,3],"e":{"x":20,"y":30}}'), A())

    def test_get_and_set_item(self):
        ti = B()
        self.assertEqual(ti["c"], 30)
        ti["c"] = 60
        self.assertEqual(ti["c"], 60)
        self.assertEqual(ti["g.x"], 20)
        ti["g.x"] = 50
        self.assertEqual(ti["g.x"], 50)
        self.assertRaises(KeyError, ti.__getitem__, "z.x")
        self.assertRaises(KeyError, ti.__setitem__, "z.x", "10")

    def test_get_members(self):
        ti0 = B()
        ti1 = C()
        values = ti1.get_values()
        ti0.set_values(values)
        self.assertEqual(ti0, ti1)
        ti2 = ti0.convert_to(C)
        self.assertEqual(ti0, ti2)

    def test_copy(self):
        from copy import copy, deepcopy
        c = C()
        cc = copy(c)
        print (c, cc)
        self.assertEqual(c, cc)
        cc.g.x = 50
        self.assertEqual(c, cc)
        cdc = deepcopy(c)
        self.assertEqual(c, cc)
        cdc.g.x = 80
        self.assertEqual(c, cc)



if __name__ == '__main__':
    unittest.main()
