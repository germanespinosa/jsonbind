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


if __name__ == '__main__':
    unittest.main()
