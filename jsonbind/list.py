from json_cpp import JsonList

from serializable import JsonSerializable
from serialization import JsonSerialization
from .search import bin_search, SearchType, SortOrder, NotFoundBehavior
import json

class JsonList(list, JsonSerializable):
    """
    An enhanced list for JSON-like data handling with type constraints.

    Attributes:
    - list_type: The allowed type for items in the list.
    - allow_empty: Flag to allow None values in the list.

    Example:
        js = JsonList(list_type=int, iterable=[1,2,3])
        print(js)           # Outputs: [1,2,3]
        js.append(4)
        print(js)           # Outputs: [1,2,3,4]
        js.append(3.4)      # Raises TypeError
        js.append(None)      # Raises TypeError


        js = JsonList(list_type=JsonObject)
        js.append(JsonObject(x=1, y=2))
        js.append(JsonObject(x=3, y=4))
        print(js)           # Outputs: [{"x":1,"y":2},{"x":3,"y":4}]
        js.append(3.4)      # Raises TypeError
        js.append(None)      # Raises TypeError

        js = JsonList(list_type=int, iterable=[1,2,3], allow_empty=True)
        print(js)           # Outputs: [1,2,3]
        js.append(4)
        print(js)           # Outputs: [1,2,3,4]
        js.append(3.4)      # Raises TypeError
        js.append(None)
        print(js)           # Outputs: [1,2,3,4,null]
    """

    def __init__(self, list_type=None, iterable=None, allow_empty: bool = False):
        """
        Initialize the JsonList with a specific type and optionally provide an initial iterable.

        Parameters:
        - list_type (type, optional): The allowed type for items in the list.
        - iterable (iterable, optional): An initial collection of items.
        - allow_empty (bool): Flag to determine if None values are allowed. Default is False.
        """
        iterable = list() if not iterable else iterable
        iter(iterable)
        map(self._typeCheck, iterable)
        list.__init__(self, iterable)
        self.list_type = list_type
        self.allow_empty = allow_empty

    @staticmethod
    def create_type(list_item_type: type, list_type_name: str = "") -> type:
        """
        Dynamically creates a new JsonList subclass for a specific item type.

        Parameters:
        - list_item_type (type): The specific type for items in the new JsonList subclass.
        - list_type_name (str, optional): A name for the new JsonList subclass. Default is an empty string.

        Returns:
        type: A new JsonList subclass type.
        """

        def __init__(self, iterable=None):
            JsonList.__init__(self, iterable=iterable, list_type=list_item_type)
        if not list_type_name:
            list_type_name = "Json_%s_list" % list_item_type.__name__
        newclass = type(list_type_name, (JsonList,), {"__init__": __init__})
        return newclass

    def format(self, format_string: str) -> str:
        """
        Formats the JsonList using a provided format string.

        Args:
            format_string (str): The format string containing placeholders that match keys in the JsonList element.

        Returns:
            str: A formatted string with placeholders replaced by their corresponding values from the JsonList element.

        Note:
            This method supports nested formatting for nested JsonList.
        """
        formatted_string = ""
        for k in self:
            if isinstance(k, JsonSerializable):
                formatted_string += k.format(format_string=format_string)
            else:
                formatted_string += format_string.format(k)
        return formatted_string

    def _typeCheck(self, val):
        """
        Internal method to check if a value matches the list's predefined type or valid JSON types.

        Parameters:
        - val: The value to check.

        Raises:
        ValueError: If the value does not match the allowed types.
        """
        if val is None and self.allow_empty:
            return
        if self.list_type:
            if self.list_type is float and type(val) is int: #json ints can also be floats
                val = float(val)
            if not isinstance(val, self.list_type):
                raise TypeError("Wrong type %s, this list can hold only instances of %s" % (val.__class__.__name,
                                                                                            self.list_type.__name__))
        else:
            if not JsonSerialization.is_valid(val):
                raise TypeError("Wrong type %s, this list can hold only %s" % (val.__class__.__name__,
                                                                               JsonSerialization.valid_types_str()))

    def __iadd__(self, other):
        """
        Append an iterable to the current list after type checking.

        Args:
            other (iterable): The iterable to be appended to the list.

        Raises:
            TypeError: If the provided value is not of the list type.
        """
        map(self._typeCheck, other)
        list.__iadd__(self, other)
        return self

    def __add__(self, other):
        """
        Concatenates an iterable to the current list after type checking.

        Args:
            other (iterable): The iterable to be appended to the list.

        Raises:
            TypeError: If the provided value is not of the list type.

        Returns:
            A new list with the iterable concatenated to the current list
        """
        iterable = [item for item in self] + [item for item in other]
        return JsonList(list_type=self.list_type, iterable=iterable)

    def __radd__(self, other):
        """
        Concatenates the current list to an iterable after type checking.

        Args:
            other (iterable): The iterable to be appended to the list.

        Raises:
            TypeError: If the provided value is not of the list type.

        Returns:
            A new list with the current list concatenated to the iterable
        """
        iterable = [item for item in other] + [item for item in self]
        if isinstance(other, JsonList):
            return self.__class__(list_type=other.list_type, iterable=iterable)
        return JsonList(list_type=self.list_type, iterable=iterable)

    def __setitem__(self, index, value):
        """
        Set an item of the list to a given an index after type checking.

        Args:
            key (int): The index of the item.
            iterable (iterable): The iterable whose values are to be set in the slice.

        Raises:
            TypeError: If the value type is not the same as the list type.
        """
        itervalue = (value,)
        if isinstance(index, slice):
            iter(value)
            itervalue = value
        map(self._typeCheck, itervalue)
        list.__setitem__(self, index, value)

    def __setslice__(self, i, j, iterable):
        """
        Set a slice of the list to a given iterable after type checking.

        Args:
            i (int): The starting index of the slice.
            j (int): The ending index of the slice.
            iterable (iterable): The iterable whose values are to be set in the slice.

        Raises:
            TypeError: If the iterable contains values not of the list type.
        """
        iter(iterable)
        map(self._typeCheck, iterable)
        list.__setslice__(self, i, j, iterable)

    def append(self, val):
        """
        Append a value to the list after type checking.

        Args:
            val (any): The value to be appended to the list.

        Raises:
            TypeError: If the provided value is not of the list type.
        """
        self._typeCheck(val)
        list.append(self, val)

    def extend(self, iterable):
        """
        Extend the list with values from an iterable after type checking.

        Args:
            iterable (iterable): The iterable whose values are to be added to the list.

        Raises:
            TypeError: If the iterable contains values not of the list type.
        """
        iter(iterable)
        map(self._typeCheck, iterable)
        list.extend(self, iterable)

    def insert(self, i, val):
        """
        Insert a value at a specified index in the list after type checking.

        Args:
            i (int): The index where the value is to be inserted.
            val (any): The value to be inserted into the list.

        Raises:
            TypeError: If the provided value is not of the list type.
        """
        self._typeCheck(val)
        list.insert(self, i, val)

    def __str__(self):
        """
        Provide a string representation of the list.

        Returns:
        str: A JSON-formatted string representation of the list.
        """
        return "[" + ",".join([JsonSerialization.serialize(x) for x in self]) + "]"

    def __repr__(self):
        """
        Official string representation of the object, used for debugging and development.

        Returns:
        str: A JSON-formatted string representation of the list.
        """
        return str(self)

    def get(self, m):
        """
        Get values associated with the specified attribute for items in the list.

        Parameters:
        - m (str): The attribute name.

        Returns:
        JsonList: A new list containing the values associated with the specified attribute.
        """
        l = JsonList()
        for i in self:
            if m in vars(i):
                l.append(vars(i)[m])
        return l

    def split_by(self, m) -> dict:
        """
        Split the list into multiple lists based on the value of a specified attribute or a calculated field.

        Parameters:
        - m (callable): The function to compute the calculated field, must receive an item from the list.
        Returns:
        dict: A dictionary where keys are unique attribute or calculated field values and values are lists of items.
        """
        r = {}
        for i in self:
            l = m(i)
            if l not in r:
                r[l] = self.__class__()
                self.list_type = self.list_type
            r[l].append(i)
        return r

    def filter(self, key):
        """
        Filter the list based on a given function.

        Parameters:
        - key (Callable): A function that takes an item as an argument and returns a boolean.

        Returns:
        JsonList: A new list containing items for which the function returned True.
        """
        nl = self.__class__()
        for i in self:
            if key(i):
                nl.append(i)
        return nl

    def find_first(self, key, not_found_behavior=NotFoundBehavior.RaiseError):
        """
        Find the first item in the list that meets a specified condition.

        Parameters:
        - key (Any): A value or function to search for.
        - not_found_behavior (NotFoundBehavior): Determines the behavior when the item is not found.

        Returns:
        Any: The first item that meets the condition or a behavior based on the NotFoundBehavior.
        """
        i = self.find_first_index(key, not_found_behavior=not_found_behavior)
        return None if i is None else JsonList.__getitem__(self, i)

    def find_first_index(self, key, not_found_behavior=NotFoundBehavior.RaiseError):
        """
        Find the index of the first item in the list that meets a specified condition.

        Parameters:
        - key (Any): A value or function to search for.
        - not_found_behavior (NotFoundBehavior): Determines the behavior when the item is not found.

        Returns:
        int or None: The index of the first item that meets the condition or None based on the NotFoundBehavior.
        """
        if callable(key):
            for ix, i in enumerate(self):
                if key(i):
                    return ix
        else:
            for ix, i in enumerate(self):
                if key == i:
                    return ix

        if not_found_behavior == NotFoundBehavior.RaiseError:
            raise RuntimeError("Value not found")
        else:
            return None

    def find_ordered(self,
                     value,
                     key=None,
                     search_type: SearchType = SearchType.Exact,
                     order: SortOrder = SortOrder.Ascending,
                     not_found_behavior: NotFoundBehavior = NotFoundBehavior.RaiseError):
        """
        Search for an item in an ordered list.

        Parameters:
        - value (Any): The value to search for.
        - key (Callable, optional): A function that takes an item as argument and returns a value for comparison.
        - search_type (SearchType): Type of search (e.g., exact match).
        - order (SortOrder): The ordering of the list (ascending or descending).
        - not_found_behavior (NotFoundBehavior): Determines the behavior when the item is not found.

        Returns:
        Any: The found item or a behavior based on the NotFoundBehavior.
        """
        i = bin_search(self, value, key=key, search_type=search_type, order=order, not_found_behavior=not_found_behavior)
        return None if i is None else JsonList.__getitem__(self, i)

    def find_ordered_index(self,
                           value,
                           key=None,
                           search_type: SearchType = SearchType.Exact,
                           order: SortOrder = SortOrder.Ascending,
                           not_found_behavior: NotFoundBehavior = NotFoundBehavior.RaiseError):
        """
        Search for the index of an item in an ordered list.

        Parameters:
        - value (Any): The value to search for.
        - key (Callable, optional): A function that takes an item as argument and returns a value for comparison.
        - search_type (SearchType): Type of search (e.g., exact match).
        - order (SortOrder): The ordering of the list (ascending or descending).
        - not_found_behavior (NotFoundBehavior): Determines the behavior when the item is not found.

        Returns:
        int or None: The index of the found item or None based on the NotFoundBehavior.
        """
        return bin_search(self,
                          value,
                          key=key,
                          search_type=search_type,
                          order=order,
                          not_found_behavior=not_found_behavior)

    def process(self, l):
        """
        Processes each element in the list using a provided function.

        Args:
            l (callable): A function to be applied to each item in the list.

        Returns:
            JsonList: A new JsonList with items after being processed by the function `l`.
        """
        nl = JsonList()
        for i in self:
            nl.append(l(i))
        return nl

    def copy(self):
        """
        Creates a deep copy of the current JsonList.

        Returns:
            JsonList: A new JsonList that is a deep copy of the current list.
        """
        return self.__class__.parse(str(self))

    def get_values(self):
        """
        Retrieves the values from the list. If an item is an instance of JsonObject or JsonList,
        recursively gets the values from the object or list.

        Returns:
            JsonList: A new JsonList containing the values from the original list.
        """
        values = JsonList(list_type=JsonList)
        for i in self:
            if isinstance(i, JsonSerializable):
                values.append(i.get_values())
            else:
                values.append(i)
        return values

    def set_values(self, values: list):
        """
        Sets the values in the current JsonList based on the provided values list.

        Args:
            values (list): The list of values to be set in the current JsonList.
        """
        for i in values:
            if issubclass(self.list_type, JsonSerializable):
                ni = self.list_type()
                ni.set_values(i)
                self.append(ni)
            else:
                self.append(i)

    def load(self, json_string: str) -> "JsonList":
        """
        Parses a JSON string or list into a JsonList. The type of items in the resulting JsonList
        is determined based on the list_type attribute of the JsonList.

        Args:
            json_string (str, optional): A JSON-formatted string to be parsed into a JsonList.
            json_list (list, optional): A list to be converted into a JsonList.

        Returns:
            JsonList: A new or updated JsonList populated with items from the provided JSON string or list.

        Raises:
            TypeError: If provided json_string is not a string or json_list is not a list.
        """
        parsed_list = json.loads(json_string)
        return self.__load_parsed_list__(parsed_list=parsed_list)

    def __load_parsed_list__(self, parsed_list: list) -> "JsonList":
        self.clear()
        it = self.list_type
        for i in parsed_list:
            if self.list_type:
                self.append(JsonSerialization.deserialize(i, it))
            else:
                if isinstance(i, list):
                    self.append(JsonList().__load_parsed_list__(parsed_list=i))
                elif isinstance(i, "JsonObject"):
                    from .object import JsonObject
                    self.append(i, JsonObject.__load_parsed_dict__(parsed_dict=i))
                elif JsonSerialization.is_valid(i):
                    self.append(i)
                else:
                    raise TypeError("Type %s is not serializable." % i.__class__.__name__)
        return self

    def save(self, file_path: str):
        """
        Save the list to a file in JSON format.

        Parameters:
        - file_path (str): The path to the file where the list will be saved.
        """
        with open(file_path, 'w') as f:
            f.write(str(self))

    def load_from_file(self, file_path: str):
        """
        Load the list from a file containing JSON data.

        Parameters:
        - file_path (str): The path to the file to load data from.
        """
        import os
        if not os.path.exists(file_path):
            return None
        json_content = ""
        with open(file_path) as f:
            json_content = f.read()
        return self.parse(json_content)

    def load_from_url(self, uri: str):
        """
        Load JSON data into the list from a URL.

        Parameters:
        - uri (str): The URL to fetch the data from.
        """
        import requests
        req = requests.get(uri)
        if req.status_code == 200:
            return self.parse(req.text)
        return None

    def to_numpy_array(self):
        """
        Convert the list to a numpy array.

        Returns:
        numpy.array: The numpy array representation of the list.

        Notes:
        Only supports conversion if the list contains simple types (int, float, bool) or JsonObject instances.
        """
        from numpy import array
        from .object import JsonObject
        if self.list_type is int or self.list_type is float or self.list_type is bool:
            return array(self)
        return array([i.get_values() for i in self if isinstance(i, JsonObject)])

    def from_numpy_array(self, a):
        """
        Populate the list from a numpy array.

        Parameters:
        - a (numpy.array): The array to load data from.

        Notes:
        Only supports loading from an array if the list's type is a JsonObject or a simple type.
        """
        self.clear()
        columns = self.list_type().get_columns()
        for row in a:
            ni = self.list_type()
            for i, c in enumerate(columns):
                ni[c] = row[i]
            self.append(ni)

    def to_dataframe(self, recursive: bool = False):
        """
        Convert the list to a pandas DataFrame.

        Parameters:
        - recursive (bool): Flag to indicate if nested objects should be recursively converted to DataFrame columns.

        Returns:
        pandas.DataFrame: The DataFrame representation of the list.
        """
        from pandas import DataFrame
        from .object import JsonObject
        if self.list_type is JsonObject or self.list_type is None:
            if len(self) == 0:
                return DataFrame()
            if isinstance(self[0], JsonObject):
                columns = self[0].get_columns()
            else:
                raise RuntimeError("Item type cannot be loaded to dataframe")
        else:
            if issubclass(self.list_type, JsonObject):
                columns = self.list_type().get_columns()
            else:
                return DataFrame(self)

        if recursive:
            return DataFrame([i.__dataframe_values__() for i in self], columns=columns)
        else:
            return DataFrame([i.get_values() for i in self], columns=columns)

    def from_dataframe(self, df):
        """
        Populate the list from a pandas DataFrame.

        Parameters:
        - df (pandas.DataFrame): The DataFrame to load data from.
        """
        self.clear()
        columns = df.columns
        for i, row in df.iterrows():
            ni = self.list_type()
            for c in columns:
                ni[c] = row[c]
            self.append(ni)

    def into(self, cls: type):
        """
        Convert the current list into another type derived from JsonList.

        Parameters:
        - cls (type): The target JsonList derived type to convert into.

        Returns:
        JsonList: A new JsonList of the specified type with the current list's data.

        Raises:
        RuntimeError: If the provided type is not derived from JsonList.
        """
        if not issubclass(cls, JsonList):
            raise RuntimeError("type must derive from JsonList")
        nv = cls.parse(str(self))
        return nv


JsonSerialization.add_type(list,
                           lambda l: str(JsonList(iterable=l)),
                           lambda i, t: t.__load_from_parsed_values__(parsed_values=i))
