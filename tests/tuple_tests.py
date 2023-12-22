import unittest
import sys
sys.path.append('..')
from jsonbind.core import Serialization


class TupleTests(unittest.TestCase):
    def test_tuple_serialization(self):
        self.assertEqual(Serialization.serialize((1, 2, 3, 4)), '[1,2,3,4]')

    def test_tuple_deserialization(self):
        self.assertEqual(Serialization.deserialize('[1,2,3,4]', tuple), (1, 2, 3, 4))


if __name__ == '__main__':
    unittest.main()
