import sys
sys.path.append('..')
from jsonbind import JsonSerialization
import datetime
import unittest


class Bytes(unittest.TestCase):
    def test_bytes_serialization(self):
        dt = datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10, microsecond=100)
        self.assertEqual(JsonSerialization.serialize(dt),'"2020-01-01 10:10:10.000100"')

    def test_bytes_deserialization(self):
        dt = datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10, microsecond=100)
        self.assertEqual(JsonSerialization.deserialize("2020-01-01 10:10:10.000100", datetime.datetime),dt)


if __name__ == '__main__':
    unittest.main()
