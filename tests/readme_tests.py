import unittest
import sys
sys.path.append('..')


class BoundObjectTests(unittest.TestCase):

    def test_custom_datetime_binding(self):
        import jsonbind as jb
        import datetime

        class MyDateBinding(jb.TypeBinding):
            def __init__(self):
                super().__init__(json_type=dict, python_type=datetime.datetime)

            def to_json_value(self, python_value: datetime.datetime) -> dict:
                return {"year": python_value.year,
                        "month": python_value.month,
                        "day": python_value.day}

            def to_python_value(self, json_value: dict, python_type: type) -> datetime.datetime:
                return datetime.datetime(year=json_value["year"],
                                         month=json_value["month"],
                                         day=json_value["day"])

        jb.core.Bindings.set_binding(MyDateBinding())
        print(jb.dumps(datetime.datetime.now()))

        new_date = jb.loads('{"year":2025,"month":10,"day":22}', cls=datetime.datetime)
        print(new_date, type(new_date))

        jb.Bindings.set_binding(jb.bindings.DateTimeBinding(jb.bindings.DateTimeBinding.Format.time_stamp))

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
        mydate = jb.loads('"2023-12-19 15:20:18.000"', cls=datetime.datetime)
        print(mydate, type(mydate))
        mybytes=jb.loads('"SGVsbG8gV29ybGQ="', cls=bytes)
        print (mybytes, type(mybytes))

    def test_bound_class(self):
        import jsonbind as jb
        import datetime

        class MyClass(jb.bindings.BoundClass):
            def __init__(self):
                self.text = "Hello World"
                self.date = datetime.datetime.now()
                self.data = [3, 1, 4, 1, 5, 9, 2]

        my_object = MyClass()
        print(jb.dumps(my_object))
        new_object = jb.loads('{"text":"Deseralization test","date":"2023-12-23","data":[6,2,8,3,1,8,4]}', MyClass)
        print("Text: ", new_object.text, new_object.text.__class__)
        print("Date: ", new_object.date, new_object.date.__class__)
        print("Data: ", new_object.data, new_object.data.__class__)


if __name__ == '__main__':
    unittest.main()
