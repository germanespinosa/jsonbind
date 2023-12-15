import sys
sys.path.append('..')
from jsonbind import JsonSerialization, JsonTypeMapping
import unittest


class Serialization(unittest.TestCase):
    def test_is_basic_type(self):
        self.assertTrue(JsonSerialization.is_json_type(bool))
        self.assertTrue(JsonSerialization.is_json_type(None.__class__))
        self.assertTrue(JsonSerialization.is_json_type(int))
        self.assertTrue(JsonSerialization.is_json_type(float))
        self.assertTrue(JsonSerialization.is_json_type(str))
        self.assertTrue(JsonSerialization.is_json_type(dict))
        self.assertTrue(JsonSerialization.is_json_type(list))
        self.assertFalse(JsonSerialization.is_json_type(tuple))

    def test_is_mapped_type(self):
        self.assertTrue(JsonSerialization.is_mapped_type(bool))
        self.assertTrue(JsonSerialization.is_mapped_type(None.__class__))
        self.assertTrue(JsonSerialization.is_mapped_type(int))
        self.assertTrue(JsonSerialization.is_mapped_type(float))
        self.assertTrue(JsonSerialization.is_mapped_type(str))
        self.assertTrue(JsonSerialization.is_mapped_type(dict))
        self.assertTrue(JsonSerialization.is_mapped_type(list))
        self.assertFalse(JsonSerialization.is_mapped_type(tuple))

    def test_is_serializable(self):
        self.assertTrue(JsonSerialization.is_serializable(10))
        self.assertTrue(JsonSerialization.is_serializable(int))
        self.assertTrue(JsonSerialization.is_serializable(10.5))
        self.assertTrue(JsonSerialization.is_serializable(float))
        self.assertTrue(JsonSerialization.is_serializable(True))
        self.assertTrue(JsonSerialization.is_serializable(bool))
        self.assertTrue(JsonSerialization.is_serializable(None))
        self.assertTrue(JsonSerialization.is_serializable(None.__class__))
        self.assertTrue(JsonSerialization.is_serializable("hello"))
        self.assertTrue(JsonSerialization.is_serializable(str))
        self.assertTrue(JsonSerialization.is_serializable({"a":1}))
        self.assertTrue(JsonSerialization.is_serializable(dict))
        self.assertFalse(JsonSerialization.is_serializable(tuple))
        self.assertFalse(JsonSerialization.is_serializable((1,2,3)))

    def test_is_deserializable(self):
        self.assertTrue(JsonSerialization.is_deserializable(10))
        self.assertTrue(JsonSerialization.is_deserializable(int))
        self.assertTrue(JsonSerialization.is_deserializable(10.5))
        self.assertTrue(JsonSerialization.is_deserializable(float))
        self.assertTrue(JsonSerialization.is_deserializable(True))
        self.assertTrue(JsonSerialization.is_deserializable(bool))
        self.assertTrue(JsonSerialization.is_deserializable(None))
        self.assertTrue(JsonSerialization.is_deserializable(None.__class__))
        self.assertTrue(JsonSerialization.is_deserializable("hello"))
        self.assertTrue(JsonSerialization.is_deserializable(str))
        self.assertTrue(JsonSerialization.is_deserializable({"a":1}))
        self.assertTrue(JsonSerialization.is_deserializable(dict))
        self.assertFalse(JsonSerialization.is_deserializable(tuple))
        self.assertFalse(JsonSerialization.is_deserializable((1,2,3)))

    def test_serialize(self):
        self.assertEqual(JsonSerialization.serialize(1), "1")
        self.assertEqual(JsonSerialization.serialize(1.3), "1.3")
        self.assertEqual(JsonSerialization.serialize(True), "true")
        self.assertEqual(JsonSerialization.serialize(False), "false")
        self.assertEqual(JsonSerialization.serialize(None), "null")
        self.assertEqual(JsonSerialization.serialize("Hello"), '"Hello"')
        self.assertEqual(JsonSerialization.serialize({"a":1, "b":2}), '{"a": 1, "b": 2}')
        self.assertEqual(JsonSerialization.serialize([1, 2, 2.3]), '[1, 2, 2.3]')

    def test_deserialize(self):
        self.assertEqual(JsonSerialization.deserialize(1),1)
        self.assertEqual(JsonSerialization.deserialize(1.3), 1.3)
        self.assertEqual(JsonSerialization.deserialize(True), True)
        self.assertEqual(JsonSerialization.deserialize(False), False)
        self.assertEqual(JsonSerialization.deserialize(None),None)
        self.assertEqual(JsonSerialization.deserialize('Hello'), "Hello")
        self.assertEqual(JsonSerialization.deserialize({"a":1, "b":2}), {"a":1, "b":2})
        self.assertEqual(JsonSerialization.deserialize([1, 2, 2.3]), [1, 2, 2.3])

    def test_base_mapping(self):
        class MyStr(str):
            pass
        self.assertEqual(JsonSerialization.serialize(MyStr('Hello')), '"Hello"')

    def test_add_mapping(self):

        class MySpecialString:
            def __init__(self):
                self.x = 0
                self.y = 0
            @staticmethod
            def parse(s:str):
                v = s.split(',')
                ns = MySpecialString()
                ns.x = int(v[0])
                ns.y = int(v[1])
                return ns

        class MySpecialStringMapping(JsonTypeMapping):
            _mapped_type = MySpecialString
            _json_type = str
            @staticmethod
            def to_json_string(c: MySpecialString) -> str:
                return '"%i,%i"' % (c.x, c.y)

            @staticmethod
            def to_mapped_type(c: str, mapped_type: type) -> MySpecialString:
                return mapped_type.parse(c)

        JsonSerialization.add_type_mapping(MySpecialStringMapping)
        mss = MySpecialString()
        mss.x = 100
        mss.y = 200
        self.assertEqual(JsonSerialization.serialize(mss),'"100,200"')
        mss = JsonSerialization.deserialize("100,200", MySpecialString)
        self.assertEqual(mss.x, 100)
        self.assertEqual(mss.y, 200)

        class MySpecialList:
            def __init__(self):
                self.x = 0
                self.y = 0
            @staticmethod
            def parse(l:list):
                nl = MySpecialList()
                nl.x = l[0]
                nl.y = l[1]
                return nl

        class MySpecialListMapping(JsonTypeMapping):
            _mapped_type = MySpecialList
            _json_type = list
            @staticmethod
            def to_json_string(c: MySpecialList) -> str:
                return "[%i,%i]" % (c.x, c.y)

            @staticmethod
            def to_mapped_type(c: list, mapped_type: type) -> MySpecialList:
                return mapped_type.parse(c)

        JsonSerialization.add_type_mapping(MySpecialListMapping)


        mss = MySpecialList()
        mss.x = 100
        mss.y = 200
        self.assertEqual(JsonSerialization.serialize(mss),'[100,200]')
        mss = JsonSerialization.deserialize([100,200], MySpecialList)
        self.assertEqual(mss.x, 100)
        self.assertEqual(mss.y, 200)

        class MySpecialDict:
            def __init__(self):
                self.x = 0
                self.y = 0
            @staticmethod
            def parse(d:dict):
                nl = MySpecialDict()
                nl.x = d["x"]
                nl.y = d["y"]
                return nl

            @staticmethod
            def serialize(c):
                return '{"x":%i,"y":%i}' % (c.x, c.y)

        class MySpecialDictMapping(JsonTypeMapping):
            _mapped_type = MySpecialDict
            _json_type = dict
            @staticmethod
            def to_json_string(c: MySpecialDict) -> str:
                return MySpecialDict.serialize(c)

            @staticmethod
            def to_mapped_type(c: list, mapped_type: type) -> MySpecialList:
                return mapped_type.parse(c)

        JsonSerialization.add_type_mapping(MySpecialDictMapping)


        mss = MySpecialDict()
        mss.x = 100
        mss.y = 200
        self.assertEqual(JsonSerialization.serialize(mss),'{"x":100,"y":200}')
        mss = JsonSerialization.deserialize({"x":100,"y":200}, MySpecialDict)
        self.assertEqual(mss.x, 100)
        self.assertEqual(mss.y, 200)


if __name__ == '__main__':
    unittest.main()
