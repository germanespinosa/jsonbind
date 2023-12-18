from .serialization import Serialization


class Serializable(object):
    def __str__(self) -> str:
        """
        Returns a string representation of the JsonObject in JSON format.

        Returns:
            str: JSON-formatted string.
        """
        return Serialization.serialize(self)

    @classmethod
    def parse(cls, json_string: str) -> "Serializable":
        return Serialization.deserialize(json_string=json_string, python_type=cls)

    @classmethod
    def parse_from_file(cls, file_path: str) -> "Serializable":
        import os
        if not os.path.isfile(file_path):
            raise FileNotFoundError("file does not exist")
        with open(file_path, "r") as f:
            json_string = f.read()
        return cls.parse(json_string=json_string)

    @classmethod
    def parse_from_url(cls, url: str) -> "Serializable":
        import requests
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.exceptions
        json_string = response.text
        return cls.parse(json_string=json_string)



# import typing
#
# from .serialization import JsonSerialization
#
# class JsonSerializable(object):
#     @classmethod
#     def parse(cls, json_string="") -> "JsonSerializable":
#         new_value = cls()
#         new_value.load(json_string=json_string)
#         return new_value
#
#     @classmethod
#     def __load_from_parsed_values__(self, parsed_values=typing.Union[bool, float, int, str, list, dict]) -> "JsonSerializable":
#
#
#     def load(self, json_string="") -> "JsonSerializable":
#         import json
#         parsed_values = json.loads(json_string)
#         return self.__load_from_parsed_values__(parsed_values=parsed_values)
#
#     def __load_from_parsed_values__(self, parsed_values=typing.Union[list, dict]) -> "JsonSerializable":
#         raise NotImplemented("JsonSerializable is a base class, it must be inherited and parse implemented")
#
#     def format(self, format_string: str) -> str:
#         raise NotImplemented("JsonSerializable is a base class, it must be inherited and format implemented")
#
#     def get_values(self) -> list:
#         raise NotImplemented("JsonSerializable is a base class, it must be inherited and get_values implemented")
#
#     def set_values(self, values: list):
#         raise NotImplemented("JsonSerializable is a base class, it must be inherited and set_values implemented")
#
#     def __str__(self):
#         raise NotImplemented("JsonSerializable is a base class, it must be inherited and __str__ implemented")
#
#     def __repr__(self):
#         return str(self)
#
#
#
# JsonSerialization.add_type(JsonSerializable,
#                            lambda o: str(o),
#                            lambda s, t: t.__load_from_parsed_values__(parsed_values=s))