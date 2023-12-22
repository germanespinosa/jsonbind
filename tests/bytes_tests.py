import unittest
import sys
sys.path.append('..')
from jsonbind.core import Serialization


class BytesTests(unittest.TestCase):
    def test_bytes_serialization(self):
        self.assertEqual(Serialization.serialize(b"Hello"), '"SGVsbG8="')

    def test_bytes_deserialization(self):
        self.assertEqual(Serialization.deserialize('"SGVsbG8="', bytes), b"Hello")


if __name__ == '__main__':
    unittest.main()
