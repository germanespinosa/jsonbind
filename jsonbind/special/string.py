from ..core.serialization import Serialization


class JsonString(str):

    def __new__(cls, string=""):
        if string:
            try:
                o = Serialization.deserialize(json_string=string)
                instance = super().__new__(cls, str(o))
                setattr(instance, "value", o)
            except:
                instance = super().__new__(cls, string)
                setattr(instance, "value", None)
        else:
            instance = super().__new__(cls)
        return instance


