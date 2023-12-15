import typing
import json
from types import NoneType


class JsonTypeMapping:
    _json_type: type = None
    _mapped_type: type = None
    @staticmethod
    def to_json_string(c: "JsonTypeMapping") -> str:
        raise NotImplementedError("to_json_type() not implemented")

    @staticmethod
    def to_mapped_type(c: "JsonTypeMapping._json_type", mapped_type: type) -> "JsonTypeMapping._mapped_type":
        raise NotImplementedError("to_mapped_type() not implemented")


class JsonSerialization:
    _json_types = (NoneType, bool, int, float, str, dict, list)
    _mapped_types = (NoneType, bool, int, float, str, dict, list)
    _default_mapping = {NoneType:NoneType,
                        bool: bool,
                        int: int,
                        float: float,
                        str: str,
                        dict: dict,
                        list: list}
    _type_mapping = {NoneType: (NoneType,),
                     bool: (bool,),
                     int: (int,),
                     float: (float,),
                     str: (str,),
                     dict: (dict,),
                     list: (list,),}
    _serializers = {NoneType: lambda n: "null",
                    bool: lambda b: "true" if b else "false",
                    int: lambda i: str(i),
                    float: lambda f: str(f),
                    str: lambda s: json.dumps(s),
                    dict: lambda d: json.dumps(d),
                    list: lambda l: json.dumps(l)}
    _deserializers = {NoneType: lambda n, t: n,
                      bool: lambda b, t: b,
                      int: lambda i, t: i,
                      float: lambda f, t: f,
                      str: lambda s, t: s,
                      dict: lambda d, t: d,
                      list: lambda l, t:l}
    _base_map = {}

    @staticmethod
    def is_json_type(t: type) -> bool:
        return issubclass(t, JsonSerialization._json_types)

    @staticmethod
    def is_mapped_type(t: type) -> bool:
        return issubclass(t, JsonSerialization._mapped_types)

    @staticmethod
    def is_serializable(type_or_value) -> bool:
        if isinstance(type_or_value, type):
            return JsonSerialization.is_json_type(type_or_value)
        else:
            return JsonSerialization.is_json_type(type_or_value.__class__)

    @staticmethod
    def is_deserializable(type_or_value) -> bool:
        if isinstance(type_or_value, type):
            return JsonSerialization.is_mapped_type(type_or_value)
        else:
            return JsonSerialization.is_mapped_type(type_or_value.__class__)

    @staticmethod
    def serialize(value: typing.Any) -> "JsonSerialization._json_types":
        t = value.__class__
        if JsonSerialization.is_mapped_type(t):
            base = JsonSerialization.map_to_base(t)
            return JsonSerialization._serializers[base](value)
        raise TypeError("value type '%s' is not serializable" % value.__class__.__name__)

    @staticmethod
    def deserialize(json_value:typing.Any, mapped_type: type = None) -> "JsonSerialization._mapped_types":
        if JsonSerialization.is_json_type(json_value.__class__):
            if mapped_type is None:
                mapped_type = JsonSerialization._default_mapping[json_value.__class__]
            elif not issubclass(mapped_type, JsonSerialization._type_mapping[json_value.__class__]):
                raise TypeError("value type '%s' cannot be deserialized into %s" % (json_value.__class__.__name__, mapped_type.__name__))
            base = JsonSerialization.map_to_base(mapped_type)
            return JsonSerialization._deserializers[base](json_value, mapped_type)
        raise TypeError("value type '%s' is not deserializable" % json_value.__class__.__name__)

    @staticmethod
    def map_to_base(t: type) -> type:
        if t in JsonSerialization._mapped_types:
            return t
        if t in JsonSerialization._base_map:
            return JsonSerialization._base_map[t]
        for mt in JsonSerialization._mapped_types:
            if issubclass(t, mt):
                JsonSerialization._base_map[t] = mt
                return mt
        raise TypeError("type '%s' is not mapped to a json type" % t.__name__)

    @staticmethod
    def serializable() -> typing.Union:
        return typing.Union[JsonSerialization._mapped_types]

    @staticmethod
    def deserializable() -> typing.Union:
        return typing.Union[JsonSerialization._json_types]

    @staticmethod
    def add_type_mapping(mapping: type,
                         make_default: bool = False) -> None:
        if not issubclass(mapping, JsonTypeMapping):
            raise TypeError("mapping must inherit from JsonTypeMapping")

        if mapping._json_type not in JsonSerialization._json_types:
            raise TypeError("%s is not mappable" % mapping._json_type.__class__.__name__)

        JsonSerialization._mapped_types += (mapping._mapped_type,)
        JsonSerialization._type_mapping[mapping._json_type] += (mapping._mapped_type,)
        JsonSerialization._serializers[mapping._mapped_type] = mapping.to_json_string
        JsonSerialization._deserializers[mapping._mapped_type] = mapping.to_mapped_type
        if make_default:
            JsonSerialization._default_mapping[mapping._json_type] = mapping._mapped_type