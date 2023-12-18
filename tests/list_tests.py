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

if __name__ == '__main__':
    unittest.main()
