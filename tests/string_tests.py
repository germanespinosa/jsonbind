import unittest
import sys
sys.path.append('..')
from jsonbind import Serialization, Object, String


class StringTests(unittest.TestCase):

    def test_deserialization(self):
        js = Serialization.deserialize('"{\\"a\\":10,\\"b\\":20,\\"c\\":30}"', String)
        print("HERE!!!", js, js.__class__, js.value)


if __name__ == '__main__':
    unittest.main()
