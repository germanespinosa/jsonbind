import datetime
from .serialization import JsonSerialization, JsonTypeMapping

class JsonDateMapping(JsonTypeMapping):
    _json_type = str
    _mapped_type = datetime.datetime
    _date_format = '%Y-%m-%d %H:%M:%S.%f'

    @staticmethod
    def to_mapped_type(c: str, mapped_type: type) -> datetime.datetime:
        return datetime.datetime.strptime(c, JsonDateMapping._date_format)

    @staticmethod
    def to_json_string(c: datetime.datetime) -> str:
        return '"%s"' % c.strftime(JsonDateMapping._date_format)

JsonSerialization.add_type_mapping(JsonDateMapping)