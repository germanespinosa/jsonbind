import sys
sys.path.append('..')
from jsonbind import JsonSerialization
import unittest


class Bytes(unittest.TestCase):
    def test_bytes_serialization(self):
        self.assertEqual(JsonSerialization.serialize("Hello".encode("ascii")),'"SGVsbG8="')

    def test_bytes_deserialization(self):
        self.assertEqual(JsonSerialization.deserialize('"SGVsbG8="', bytes),"Hello".encode("ascii"))


if __name__ == '__main__':
    unittest.main()
