import datetime
import unittest
import sys
sys.path.append('..')
from jsonbind import Serialization, DateTimeBinding, Bindings


class DateTimeTests(unittest.TestCase):
    def test_bytes_serialization(self):
        dt = datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10, microsecond=100)
        self.assertEqual(Serialization.serialize(dt), '"2020-01-01 10:10:10.000100"')

    def test_bytes_deserialization(self):
        dt = datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10, microsecond=100)
        self.assertEqual(Serialization.deserialize('"2020-01-01 10:10:10.000100"', datetime.datetime), dt)

    def test_date_format(self):
        Bindings.set_binding(DateTimeBinding(date_format="%Y-%m-%d"))
        dt = datetime.datetime(year=2020, month=1, day=1)
        self.assertEqual(Serialization.serialize(dt), '"2020-01-01"')
        self.assertEqual(Serialization.deserialize('"2020-01-01"', datetime.datetime), dt)


if __name__ == '__main__':
    unittest.main()
