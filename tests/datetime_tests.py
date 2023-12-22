import datetime
import unittest
import sys
sys.path.append('..')
from jsonbind.core import Serialization, Bindings
from jsonbind.bindings import DateTimeBinding


class DateTimeTests(unittest.TestCase):
    def test_bytes_serialization(self):
        dt = datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10, microsecond=100)
        self.assertEqual(Serialization.serialize(dt), '"2020-01-01 10:10:10.000100"')

    def test_bytes_deserialization(self):
        dt = datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10, microsecond=100)
        self.assertEqual(Serialization.deserialize('"2020-01-01 10:10:10.000100"', datetime.datetime), dt)

    def test_date(self):
        dt = datetime.date(year=2020, month=12, day=31)
        self.assertEqual(Serialization.serialize(dt), '"2020-12-31"')
        self.assertEqual(Serialization.deserialize('"2020-12-31"', datetime.date), dt)

    def test_time(self):
        dt = datetime.time(hour=20, minute=10, second=35)
        self.assertEqual(Serialization.serialize(dt), '"20:10:35.000000"')
        self.assertEqual(Serialization.deserialize('"20:10:35.000000"', datetime.time), dt)


if __name__ == '__main__':
    unittest.main()
