import unittest
import sys
sys.path.append('..')
from jsonbind.special import List, Object
from jsonbind.addons import numpy, pandas

class NumpyAddonTests(unittest.TestCase):
    def test_to_numpy_array(self):
        l = List(list_type=Object, iterable=[Object(a=i,
                                                    b=i+10,
                                                    c=i+20,
                                                    d=Object(x=i+30,
                                                             y=i+40,
                                                             z=Object(i=i+50,
                                                                      j=i+60))) for i in range(100)])
        numpy_array = l.to_numpy_array()
        for row, item in zip(numpy_array, l):
            values = item.get_values()
            for i, (column_name, value) in enumerate(values):
                self.assertEqual(value,row[i].item())

    def test_from_numpy_array(self):
        l = List(list_type=Object, iterable=[Object(a=i,
                                                    b=i+10,
                                                    c=i+20,
                                                    d=Object(x=i+30,
                                                             y=i+40,
                                                             z=Object(i=i+50,
                                                                      j=i+60))) for i in range(100)])
        numpy_array = l.to_numpy_array()
        l2 = List.create_type(list_type=Object).from_numpy_array(numpy_array)
        self.assertEqual(l2,l)


if __name__ == '__main__':
    unittest.main()
