from .serialization import JsonSerialization, JsonTypeMapping
from enum import Enum

class JsonEnumMapping(JsonTypeMapping):
    _json_type = str
    _mapped_type = Enum

    @staticmethod
    def to_mapped_type(c: str, mapped_type: type) -> Enum:
        return mapped_type[c]

    @staticmethod
    def to_json_string(c: Enum) -> str:
        return '"%s"' % c.name

JsonSerialization.add_type_mapping(JsonEnumMapping)