import unittest
import sys
sys.path.append('..')
from jsonbind import Serialization, List, Object


class ListTests(unittest.TestCase):
    def test_list_serialization(self):
        l = List(iterable=[1, 2, 3])
        self.assertEqual(Serialization.serialize(l), '[1,2,3]')
        l = List(list_type=Object, iterable=[Object(x=1, y=2), Object(x=3, y=4)])
        self.assertEqual(Serialization.serialize(l), '[{"x":1,"y":2},{"x":3,"y":4}]')

    def test_list_deserialization(self):
        l = List(iterable=[1, 2, 3])
        self.assertEqual(Serialization.deserialize('[1,2,3]'), l)
        l = List(list_type=Object, iterable=[Object(x=1, y=2), Object(x=3, y=4)])
        self.assertEqual(Serialization.deserialize('[{"x":1,"y":2},{"x":3,"y":4}]', List.create_type(list_type=Object)), l)

    def test_list_copy(self):
        from copy import copy, deepcopy
        l = List(iterable=[1, 2, 3])
        lc = copy(l)
        self.assertEqual(l,lc)
        l = List(iterable=[1, [1,2,3], 3])
        lc = copy(l)
        self.assertEqual(l,lc)
        lc[1].append(4)
        self.assertEqual(l, lc)
        ldc = deepcopy(l)
        self.assertEqual(l, ldc)
        ldc[1].append(5)
        self.assertNotEqual(l, ldc)

    def test_list_filter(self):
        l = List(list_type=int, iterable=range(100))
        l = l.filter(lambda i: i<50)
        self.assertEqual(l, list(range(50)))
        self.assertNotEqual(l, list(range(60)))
        l = List(list_type=Object, iterable=[Object(x=x, y=x*2) for x in range(100)])
        e = l.filter(lambda o: o.x % 2)
        fl = List(list_type=Object, iterable=[Object(x=x, y=x*2) for x in range(1,100,2)])
        self.assertEqual(e, fl)

    def test_list_split(self):
        l = List(list_type=Object, iterable=[Object(x=x, y=x*2) for x in range(100)])
        s = l.split_by(lambda i: i.x % 2)
        self.assertEqual(len(s[1]), len(s[0]))
        even = l.filter(lambda i: i.x % 2 == 0)
        self.assertEqual(s[0], even)
        odd = l.filter(lambda i: i.x % 2 == 1)
        self.assertEqual(s[1], odd)

    def test_list_map(self):
        l = List(list_type=Object, iterable=[Object(x=x, y=x*2) for x in range(100)])
        m = l.map(lambda i:Object(nx=i.x + i.y, ny=float(i.x/2)))
        self.assertEqual(m, List(list_type=Object, iterable=[Object(nx=x*3, ny=x/2) for x in range(100)]))

    def test_create_test(self):
        lt = List.create_type(list_type=Object)
        l = lt()
        self.assertRaises(TypeError, l, 1)
        self.assertRaises(TypeError,l, "str")
        self.assertRaises(TypeError, l, None)

        lt = List.create_type(list_type=Object, allow_empty=True)
        l = lt()
        self.assertRaises(TypeError, l, 1)
        self.assertRaises(TypeError,l, "str")
        l.append(None)

if __name__ == '__main__':
    unittest.main()
