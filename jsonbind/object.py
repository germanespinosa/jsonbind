import typing
from .type_binding import TypeBinding, JsonTypes, Bindings
from .serializable import Serializable

Number = typing.Union[bool, int, float]


class Object(Serializable):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._output_names: typing.Dict[str, str] = dict()

    def __eq__(self, other: "Object") -> bool:
        for key, value in self.__dict__.items():
            if key not in other.__dict__:
                return False
            if other.__dict__[key] != value:
                return False
        return True

    def __copy__(self) -> "Object":
        copy = self.__class__()
        for key, value in self.__dict__.items():
            copy.__dict__[key] = value
        return copy

    def get_members(self) -> typing.List[typing.Tuple[str, typing.Any]]:
        """
        Retrieve all member variables of the JsonObject that don't start with an underscore.

        Returns:
            list: List of member attribute names.
        """
        members: typing.List[typing.Tuple[str, typing.Any]] = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            members.append((key, value))
        return members

    def get_columns(self) -> typing.List[typing.Tuple[str, type]]:
        """
        Retrieve the names of all columns contained within the JsonObject.

        Returns:
            list: List of all column names in the Object.
        """
        columns: typing.List[typing.Tuple[str, type]] = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            if isinstance(value, Object):
                columns += [(key + "." + column_name, column_type) for column_name, column_type in value.get_columns()]
            else:
                columns.append((key, value.__class__))
        return columns

    def get_numeric_columns(self) -> typing.List[typing.Tuple[str, type]]:
        """
        Retrieve the names of all numeric columns contained within the Object.

        Returns:
            list: List of all numeric column names in the Object.
        """
        columns: typing.List[typing.Tuple[str, type]] = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            if isinstance(value, Object):
                columns += [(key + "." + column_name, column_type) for column_name, column_type in value.get_numeric_columns()]
            else:
                if isinstance(value, Number):
                    columns.append((key, value.__class__))
        return columns

    def get_values(self) -> typing.List[typing.Tuple[str, typing.Any]]:
        """
        Retrieve all values contained within the JsonObject.

        Returns:
            JsonList: List containing all values from the JsonObject.
        """
        values = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            if isinstance(value, Object):
                values += [(key + "." + column_name, column_value) for column_name, column_value in value.get_values()]
            else:
                values.append((key, value))
        return values

    def get_numeric_values(self) -> typing.List[typing.Tuple[str, Number]]:
        """
        Retrieve numeric values contained within the JsonObject.

        Returns:
            JsonList: List containing numeric values from the JsonObject.
        """
        values: typing.List[typing.Tuple[str, Number]] = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            if isinstance(value, Object):
                values += [(key + "." + column_name, column_value) for column_name, column_value in value.get_numeric_values()]
            else:
                if isinstance(value, Number):
                    values.append((key, value))
        return values

    def set_values(self, values: typing.List[typing.Tuple[str, typing.Any]]):
        """
        Set values for the Object given a list of values.

        Parameters:
            values (list): List of values to set in the JsonObject.

        """
        for column_name, column_value in values:
            Object.__setitem__(self, column_name, column_value)

    def convert_to(self, cls: type) -> "Object":
        """
        Convert the current jsonbind.Object into an instance of another jsonbind.Object-derived class.

        Parameters:
            cls (type): The target jsonbind.Object-derived class to convert to.

        Returns:
            JsonObject-derived instance: The converted object.

        Raises:
            RuntimeError: If provided type does not derive from JsonObject.
        """
        if not issubclass(cls, Object):
            raise RuntimeError("type must derive from jsonbind.Object")
        values = self.get_values()
        nv = cls()
        nv.set_values(values=values)
        return nv

    def __getitem__(self, key: str) -> typing.Any:
        """
        Retrieve the value associated with a given key or nested key.

        Parameters:
            key (str): The attribute name or nested key to retrieve.

        Returns:
            Any: Value associated with the key.
        """
        pos = key.find(".")
        if pos >= 0:
            child_key = key[pos+1:]
            key = key[:pos]
            if key not in self.__dict__:
                raise KeyError("key '{}' not found".format(key))
            child = self.__dict__[key]
            if isinstance(child, Object):
                return Object.__getitem__(self=child,
                                          key=child_key)
            else:
                raise KeyError("key '{}' not found".format(child_key))
        else:
            if key not in self.__dict__:
                raise KeyError("key '{}' not found".format(key))
            return self.__dict__[key]

    def __setitem__(self, key, value):
        """
        Set the value associated with a given key or nested key.

        Parameters:
            key (str): The attribute name or nested key to assign a value to.
            value (Any): The value to set for the given key.
        """
        pos = key.find(".")
        if pos >= 0:
            child_key = key[pos+1:]
            key = key[:pos]
            if key not in self.__dict__:
                raise KeyError("key '{}' not found".format(key))
            child = self.__dict__[key]
            if isinstance(child, Object):
                return Object.__setitem__(self=child,
                                          key=child_key,
                                          value=value)
            else:
                raise KeyError("key '{}' not found".format(child_key))
        else:
            setattr(self, key, value)


class ObjectBinding(TypeBinding):
    def __init__(self):
        super().__init__(json_type=dict, python_type=Object)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        json_value = dict()
        for member_name in vars(python_value):
            if member_name.startswith('_'):
                continue
            member = getattr(python_value, member_name)
            member_type = member.__class__
            bond = Bindings.get_binding(member_type)
            if not bond:
                raise TypeError("no binding found for member {} of type {}".format(member_name, member_type.__name__))
            json_value[member_name] = bond.to_json_value(getattr(python_value, member_name))
        return json_value

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        python_value = python_type()
        for member_name, member_json_value in json_value.items():
            if member_name in python_value.__dict__:
                member = getattr(python_value, member_name)
                member_type = member.__class__
                member_python_value = Bindings.to_python_value(json_value=member_json_value,
                                                               python_type=member_type)
                setattr(python_value, member_name, member_python_value)
            else:
                setattr(python_value, member_name, member_json_value)
        return python_value


Bindings.set_binding(ObjectBinding())

