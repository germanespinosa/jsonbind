from ..core.serialization import Serialization


class String(str):

    def __new__(cls, json_string=""):
        if json_string:
            try:
                o = Serialization.deserialize(json_string=json_string)
                instance = super().__new__(cls, str(o))
                setattr(instance, "value", o)
            except:
                instance = super().__new__(cls, json_string)
                setattr(instance, "value", None)
        else:
            instance = super().__new__(cls)
        return instance

