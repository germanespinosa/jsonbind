from .object import JsonObject

class JsonString(str):
    """
    A subclass of the built-in `str` class to represent JSON-formatted strings.

    This class tries to convert a given string into a JSON object upon instantiation.
    If the conversion is successful, the internal representation is a stringified version
    of the JSON object, and the original JSON object is saved as the 'value' attribute.
    If the conversion fails, the original string is preserved, and the 'value' attribute is set to None.

    Attributes:
        value (JsonObject): Parsed JSON object if successful, else None.

    Example:
        js = JsonString('{"my_attribute": "my_attribute_value"}')
        print(js)           # Outputs: {"my_attribute": "my_attribute_value"}
        print(js.value.my_attribute)     # Outputs: "my_attribute_value"


        invalid_js = JsonString('invalid_json_string')
        print(invalid_js)   # Outputs: "invalid_json_string"
        print(invalid_js.value)  # Outputs: None
    """
    def __new__(cls, string=""):
        """
        Create a new instance of the JsonString.

        Args:
            string (str, optional): The string representation of a JSON object. Defaults to an empty string.

        Returns:
            JsonString: An instance of the JsonString class.
        """
        if string:
            try:
                o = JsonObject.load(string)
                instance = super().__new__(cls, str(o))
                setattr(instance, "value", o)
            except:
                instance = super().__new__(cls, string)
                setattr(instance, "value", None)
        else:
            instance = super().__new__(cls)
        return instance


