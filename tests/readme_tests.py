import unittest
import sys
sys.path.append('..')


class BoundObjectTests(unittest.TestCase):

    def test_standard_loads(self):
        import jsonbind as jb
        mydict = jb.loads('{"name":"German Espinosa","age":41,"weight":190.0}')
        print(mydict, type(mydict))
        mylist = jb.loads('[1, 2, 3, 4]')
        print(mylist, type(mylist))
        myint = jb.loads('1')
        print(myint, type(myint))
        myfloat = jb.loads('10.5')
        print(myfloat, type(myfloat))
        mystring = jb.loads('"Hello World"')
        print(mystring, type(mystring))
        mybool = jb.loads('true')
        print(mybool, type(mybool))

    def test_standard_dumps(self):
        import jsonbind as jb
        mydict = {"name":"German Espinosa","age":41,"weight":190.0}
        print(jb.dumps(mydict), type(mydict))
        mylist = [1, 2, 3, 4]
        print(jb.dumps(mylist), type(mylist))
        myint = 1
        print(jb.dumps(myint), type(myint))
        myfloat = 10.5
        print(jb.dumps(myfloat), type(myfloat))
        mystring = "Hello World"
        print(jb.dumps(mystring), type(mystring))
        mybool = True
        print(jb.dumps(mybool), type(mybool))

    def test_non_standard_loads(self):
        import jsonbind as jb
        mytuple = jb.loads('[1, 2, 3, 4]', cls=tuple)
        print(mytuple, type(mytuple))
        myset = jb.loads('[1, 2, 3, 4]', cls=set)
        print(myset, type(myset))
        import datetime
        mydate = jb.loads('"2023-12-19"', cls=datetime.datetime)
        print(mydate, type(mydate))
        mybytes=jb.loads('"SGVsbG8gV29ybGQ="', cls=bytes)
        print (mybytes, type(mybytes))



if __name__ == '__main__':
    unittest.main()
