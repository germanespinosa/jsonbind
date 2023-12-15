from .serialization import JsonSerialization, JsonTypeMapping

class JsonBytesMapping(JsonTypeMapping):
    _json_type = str
    _mapped_type = bytes

    @staticmethod
    def to_mapped_type(c: str, mapped_type: type) -> bytes:
        import base64
        return base64.b64decode(c)

    @staticmethod
    def to_json_string(c: bytes) -> str:
        import base64
        return '"%s"' % base64.b64encode(c).decode("ascii")

JsonSerialization.add_type_mapping(JsonBytesMapping)