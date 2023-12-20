from jsonbind.core.serialization import Serialization


def loads(json_string: str, cls: type=None):
    return Serialization.deserialize(json_string=json_string, python_type=cls)

def load(fp):
    json_string = fp.read()
    return loads(json_string)

def dumps(obj,
          skipkeys=False,
          ensure_ascii=True,
          check_circular=True,
          allow_nan=True,
          cls=None,
          indent=None,
          separators=(',', ':'),
          default=None,
          sort_keys=False,
          **kw):
    return Serialization.serialize(python_value=obj,
                                   cls=cls,
                                   skipkeys=skipkeys,
                                   ensure_ascii = ensure_ascii,
                                   check_circular = check_circular,
                                   allow_nan = allow_nan,
                                   indent = indent,
                                   separators = separators,
                                   default = default,
                                   sort_keys = sort_keys,
                                   **kw)


def dump(obj,
         fp,
         skipkeys=False,
         ensure_ascii=True,
         check_circular=True,
         allow_nan=True,
         cls=None,
         indent=None,
         separators=(',', ':'),
         default=None,
         sort_keys=False, **kw):
    json_string = dumps(obj=obj,
                        skipkeys=skipkeys,
                        ensure_ascii=ensure_ascii,
                        check_circular=check_circular,
                        allow_nan=allow_nan,
                        cls=cls,
                        indent=indent,
                        separators=separators,
                        default=default,
                        sort_keys=sort_keys,
                        **kw)
    return fp.write(json_string.encode("utf8"))
