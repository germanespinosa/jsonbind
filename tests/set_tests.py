import unittest
import sys
sys.path.append('..')
from jsonbind import Serialization


class SetTests(unittest.TestCase):
    def test_tuple_serialization(self):
        self.assertEqual(Serialization.serialize(set([1, 2, 3, 4])), '[1,2,3,4]')

    def test_tuple_deserialization(self):
        self.assertEqual(Serialization.deserialize('[1,2,3,4]', set), set([1, 2, 3, 4]))


if __name__ == '__main__':
    unittest.main()
