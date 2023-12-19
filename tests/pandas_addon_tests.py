import unittest
import sys
sys.path.append('..')
from jsonbind import Object, List
from jsonbind.addons import pandas

class PandasAddonTests(unittest.TestCase):
    def test_pandas_to_data_series(self):
        o = Object(a=123,
                   b=456,
                   c=789,
                   d=Object(x=123,
                            y=456,
                            z=Object(i=123,
                                     j=456)),
                   e=List(list_type=Object, iterable=[Object(p=o*4,
                                                             o=o*10,
                                                             q=Object(z=o,
                                                                      p=2)) for o in range(10)]))
        dt = o.to_data_series()
        self.assertEqual(dt["a"], 123)
        self.assertEqual(dt["b"], 456)
        self.assertEqual(dt["c"], 789)
        self.assertEqual(dt["d.x"], 123)
        self.assertEqual(dt["d.y"], 456)
        self.assertEqual(dt["d.z.i"], 123)
        self.assertEqual(dt["d.z.j"], 456)
        self.assertEqual(dt["e"]["p"][1], 4)
        self.assertEqual(dt["e"]["o"][1], 10)
        self.assertEqual(dt["e"]["q.z"][1], 1)
        self.assertEqual(dt["e"]["q.p"][1], 2)
        l = List(list_type=Object, iterable=[Object(a=i,
                                                    b=i+10,
                                                    c=i+20,
                                                    d=Object(x=i+30,
                                                             y=i+40,
                                                             z=Object(i=i+50,
                                                                      j=i+60))) for i in range(100)])
        data_frame = l.to_data_frame()

        for i, row in data_frame.iterrows():
            o = l[i]
            values = o.get_values()
            for column_name, value_name in values:
                self.assertEqual(o[column_name],row[column_name].item())

    def test_pandas_from_data_series(self):
        l = List(list_type=Object, iterable=[Object(a=i,
                                                    b=i+10,
                                                    c=i+20,
                                                    d=Object(x=i+30,
                                                             y=i+40,
                                                             z=Object(i=i+50,
                                                                      j=i+60))) for i in range(100)])
        df = l.to_data_frame()
        l2 = List.create_type(list_type=Object).from_data_frame(df)
        self.assertEqual(l2,l)


if __name__ == '__main__':
    unittest.main()
