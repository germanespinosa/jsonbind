#
#
# import json
# import typing
# from datetime import datetime
# import requests
# from os import path
# import base64
#
# from .util import check_type
# from .decorators import classorinstancemethod
# from .datetime import JsonDate
# from .serializable import JsonSerializable
# from .serialization import JsonSerialization
# from enum import Enum
#
#
# class JsonParseBehavior(Enum):
#     RaiseError = 0
#     IgnoreNewAttributes = 1
#     IncorporateNewAttributes = 2
#
#
# class JsonObject(object, JsonSerializable):
#     """
#     A generic object to represent and manipulate JSON-like data structures.
#     """
#     def __init__(self, *args, **kwargs):
#         """
#         Initialize a new instance of JsonObject.
#
#         Parameters:
#         - args (tuple): Optional argument, typically a JSON string.
#         - kwargs (dict): Keyword arguments representing members of the object.
#
#         Example:
#         js = JsonObject(my_attribute1="str_value", my_attribute2=1, my_attribute3=5.2, my_attribute4=True, my_attribute2=DateTime(2023,10,30))
#         print(js)           # Outputs: '{"my_attribute1":"str_value","my_attribute2":1,"my_attribute3":5.2,"my_attribute4":true,"my_attribute5":"2023-10-30 00:00:00.000000"}'
#
#         """
#         if args:
#             if type(args[0]) is str:
#                 parsed = JsonObject.load(args[0])
#                 JsonObject.__init__(self, **parsed.to_dict())
#         if type(self) is JsonObject:
#             for key, value in kwargs.items():
#                 setattr(self, key, value)
#
#         self._force_include = None
#
#     def __str__(self):
#         """
#         Returns a string representation of the JsonObject in JSON format.
#
#         Returns:
#             str: JSON-formatted string.
#         """
#         s = ""
#         for k in self.get_members():
#             if s:
#                 s += ","
#             s += "\"%s\":" % k
#             i = JsonObject.__getitem__(self, k)
#             s += JsonSerialization.serialize(i)
#         return "{%s}" % s
#
#     def get_numeric_values(self):
#         """
#         Retrieve numeric values contained within the JsonObject.
#
#         Returns:
#             JsonList: List containing numeric values from the JsonObject.
#         """
#         from .list import JsonList
#         values = JsonList()
#         for k in self.get_numeric_columns():
#             values.append(JsonObject.__getitem__(self, k))
#         return values
#
#     def get_values(self):
#         """
#         Retrieve all values contained within the JsonObject.
#
#         Returns:
#             JsonList: List containing all values from the JsonObject.
#         """
#         from list import JsonList
#         values = JsonList()
#         for k in self.get_columns():
#             value = JsonObject.__getitem__(self, k)
#             if isinstance(value, JsonList):
#                 values.append(value.get_values())
#             else:
#                 values.append(value)
#         return values
#
#     def set_values(self, values: list):
#         """
#         Set values for the JsonObject given a list of values.
#
#         Parameters:
#             values (list): List of values to set in the JsonObject.
#
#         Returns:
#             list: The provided list of values.
#
#         Raises:
#             RuntimeError: If mismatch in expected and received values.
#         """
#         columns = self.get_columns()
#         if len(columns) != len(values):
#             if len(columns) < len(values):
#                 raise RuntimeError("Not enough values to populate JsonObject. Expected: %i, Received: %i" % (len(columns), len(values)))
#             else:
#                 raise RuntimeError("Too many values to populate JsonObject. Expected: %i, Received: %i" % (len(columns), len(values)))
#         from list import JsonList
#         for i, k in enumerate(self.get_columns()):
#             if isinstance(JsonObject.__getitem__(self, k), JsonList):
#                 JsonObject.__getitem__(self, k).set_values(values[i])
#             else:
#                 JsonObject.__setitem__(self, k, values[i])
#         return values
#
#     def get_numeric_columns(self):
#         """
#         Retrieve the names of columns containing numeric values.
#
#         Returns:
#             JsonList: List of column names with numeric values.
#         """
#         from list import JsonList
#         columns = JsonList(list_type=str)
#         for v in self.get_members():
#             if isinstance(JsonObject.__getitem__(self, v), JsonObject):
#                 columns += [v + "." + c for c in self[v].get_numeric_columns()]
#             else:
#                 i = JsonObject.__getitem__(self, v)
#                 t = type(i)
#                 if t is float or t is int or t is bool:
#                     columns.append(v)
#         return columns
#
#     def into(self, cls: type,
#              behavior: JsonParseBehavior = JsonParseBehavior.RaiseError):
#         """
#         Convert the current JsonObject into an instance of another JsonObject-derived class.
#
#         Parameters:
#             cls (type): The target JsonObject-derived class to convert to.
#
#         Returns:
#             JsonObject-derived instance: The converted object.
#
#         Raises:
#             RuntimeError: If provided type does not derive from JsonObject.
#         """
#         if not issubclass(cls, JsonObject):
#             raise RuntimeError("type must derive from JsonObject")
#         nv = cls.parse(json_string=str(self), behavior=behavior)
#         return nv
#
#     def get_columns(self):
#         """
#         Retrieve the names of all columns contained within the JsonObject.
#
#         Returns:
#             JsonList: List of all column names in the JsonObject.
#         """
#         from list import JsonList
#         columns = JsonList(list_type=str)
#         for v in self.get_members():
#             if isinstance(JsonObject.__getitem__(self, v), JsonObject):
#                 columns += [v + "." + c for c in JsonObject.__getitem__(self, v).get_columns()]
#             else:
#                 columns.append(v)
#         return columns
#
#     def __repr__(self):
#         """
#         Returns a string representation of the JsonObject for debugging purposes.
#
#         Returns:
#             str: String representation of the JsonObject.
#         """
#         return str(self)
#
#     def __eq__(self, other):
#         """
#         Check equality with another JsonObject.
#
#         Parameters:
#             other (JsonObject): Another JsonObject instance to compare with.
#
#         Returns:
#             bool: True if both objects are equal, False otherwise.
#         """
#         if type(self) is not type(other):
#             return False
#         for k in self.get_members():
#             if self[k] != other[k]:
#                 return False
#         return True
#
#     def __getitem__(self, key):
#         """
#         Retrieve the value associated with a given key or nested key.
#
#         Parameters:
#             key (str): The attribute name or nested key to retrieve.
#
#         Returns:
#             Any: Value associated with the key.
#         """
#         if "." in key:
#             parts = key.split(".")
#             new_key = ".".join(parts[1:])
#             key = parts[0]
#             return JsonObject.__getitem__(JsonObject.__getitem__(self, key), new_key)
#         else:
#             return getattr(self, key)
#
#     def __setitem__(self, key, value):
#         """
#         Set the value associated with a given key or nested key.
#
#         Parameters:
#             key (str): The attribute name or nested key to assign a value to.
#             value (Any): The value to set for the given key.
#         """
#         if "." in key:
#             parts = key.split(".")
#             new_key = ".".join(parts[1:])
#             key = parts[0]
#             JsonObject.__setitem__(JsonObject.__getitem__(self, key), new_key, value)
#         else:
#             setattr(self, key, value)
#
#     def __iter__(self):
#         """
#         Return an iterator over the columns of the JsonObject.
#
#         Returns:
#             Iterator: Iterator over the JsonObject columns.
#         """
#         for k in self.get_members():
#             yield k
#
#     def force_include(self, member_name: str):
#         """
#         Adds the specified member name to list of hidden members forced during the serialization.
#
#         This method is used to append a member name to the `_force_include` list attribute of the class.
#         If `_force_include` is already initialized (i.e., not None), the `member_name` is appended to it.
#         If `_force_include` is not initialized (i.e., None), it is first initialized as a list with the `member_name` as its first element.
#
#         Parameters:
#         member_name (str): The name of the member to be added to the `_force_include` list.
#
#         Returns:
#         None: This method does not return any value. It updates the `_force_include` list in place.
#         """
#         if self._force_include:
#             self._force_include.append(member_name)
#         else:
#             self._force_include = [member_name]
#
#     def get_members(self):
#         """
#         Retrieve all member variables of the JsonObject that don't start with an underscore.
#
#         Returns:
#             list: List of member attribute names.
#         """
#         members = []
#         v = vars(self)
#         for k in v:
#             if not k:
#                 continue
#             if k[0] == "_":
#                 if self._force_include:
#                     if k not in self._force_include:
#                         continue
#                 else:
#                     continue
#             members.append(k)
#         return members
#
#     def copy(self):
#         """
#         Return a deep copy of the current JsonObject.
#
#         Returns:
#             JsonObject: A deep copy of the current object.
#         """
#         return self.__class__.parse(str(self))
#
#     def format(self, format_string: str):
#         """
#         Formats the JsonObject using a provided format string.
#
#         Args:
#             format_string (str): The format string containing placeholders that match keys in the JsonObject.
#
#         Returns:
#             str: A formatted string with placeholders replaced by their corresponding values from the JsonObject.
#
#         Note:
#             This method supports nested formatting for nested JsonObjects.
#         """
#         for k in self.get_members():
#             if not isinstance(JsonObject.__getitem__(self, k), JsonSerializable):
#                 continue
#             pos = format_string.find("{"+k+":")
#             if pos >= 0:
#                 sub_format_start = format_string.find(":", pos) + 1
#                 sub_format_end = sub_format_start
#                 bracket_count = 1
#                 while bracket_count and sub_format_end < len(format_string):
#                     c = format_string[sub_format_end]
#                     if c == '{':
#                         bracket_count += 1
#                     if c == '}':
#                         bracket_count -= 1
#                     sub_format_end += 1
#                 sub_format = format_string[sub_format_start:sub_format_end-1]
#                 sub_str = JsonObject.__getitem__(self, k).format(sub_format)
#                 format_string = format_string[:pos] + sub_str + format_string[sub_format_end:]
#         return format_string.format(**vars(self))
#
#
#     def __load_parsed_dict__(self,
#                              parsed_values: typing.Union[dict, list]) -> "JsonObject":
#         if type(parsed_values) is list:
#             self.set_values(parsed_values)
#         else:
#             for key in parsed_values:
#                 if hasattr(self, key):
#                     member = getattr(self, key)
#                     it = type(member)
#                     if issubclass(it, JsonSerializable):
#                         av = it.__load_from_parsed_values__(parsed_values=parsed_values[key])
#                     elif JsonSerialization.is_valid(it):
#                         av = JsonSerialization.deserialize()
#                     elif it is datetime:
#                         av = datetime.strptime(parsed_values[key], JsonDate.date_format)
#                     elif it is bytes:
#                         av = base64.b64decode(parsed_values[key])
#                     else:
#                         av = it(parsed_values[key])
#                     setattr(self, key, av)
#                 else:
#                     if isinstance(json_dictionary[key], (dict, list)):
#                         av = JsonObject.load(json_dictionary_or_list=json_dictionary[key])
#                         setattr(new_object, key, av)
#                     else:
#                         setattr(new_object, key, json_dictionary[key])
#
#
#     @staticmethod
#     def load(json_string: str = "", json_dictionary_or_list=None):
#         """
#         Load a JSON string or dictionary/list into a JsonObject or JsonList instance.
#
#         Args:
#             json_string (str, optional): A JSON formatted string to be loaded.
#             json_dictionary_or_list (dict or list, optional): A dictionary or list containing the JSON data.
#
#         Returns:
#             JsonObject or JsonList: A populated JsonObject or JsonList instance.
#
#         Raises:
#             TypeError: If the provided json_dictionary_or_list is neither a dictionary nor a list.
#         """
#         if json_string:
#             check_type(json_string, str, "wrong type for json_string")
#             json_dictionary_or_list = json.loads(json_string)
#         if isinstance(json_dictionary_or_list, list):
#             new_list = JsonList(list_type=None)
#             for item in json_dictionary_or_list:
#                 if isinstance(item, list) or isinstance(item, dict):
#                     new_item = JsonObject.load(json_dictionary_or_list=item)
#                 else:
#                     new_item = item
#                 new_list.append(new_item)
#             return new_list
#         elif isinstance(json_dictionary_or_list, dict):
#             new_object = JsonObject()
#             for key in json_dictionary_or_list.keys():
#                 if isinstance(json_dictionary_or_list[key], dict) or isinstance(json_dictionary_or_list[key], list):
#                     setattr(new_object, key, JsonObject.load(json_dictionary_or_list=json_dictionary_or_list[key]))
#                 else:
#                     setattr(new_object, key, json_dictionary_or_list[key])
#             return new_object
#         else:
#             raise TypeError("wrong type for json_dictionary_or_list")
#
#     def save(self, file_path: str):
#         """
#         Save the JsonObject to a file in JSON format.
#
#         Args:
#             file_path (str): Path to the file where the JsonObject should be saved.
#         """
#         with open(file_path, 'w') as f:
#             f.write(str(self))
#
#     @classmethod
#     def load_from_file(cls, file_path: str):
#         """
#         Load a JsonObject from a file containing a JSON string.
#
#         Args:
#             file_path (str): Path to the file containing the JSON data.
#
#         Returns:
#             JsonObject or None: A populated JsonObject instance or None if the file doesn't exist.
#         """
#         if not path.exists(file_path):
#             return None
#         json_content = ""
#         with open(file_path) as f:
#             json_content = f.read()
#         if cls is JsonObject:
#             return cls.load(json_content)
#         else:
#             return cls.parse(json_content)
#
#     @classmethod
#     def load_from_url(cls, uri: str):
#         """
#         Load a JsonObject from a web URL containing a JSON string.
#
#         Args:
#             uri (str): The web URL pointing to the JSON data.
#
#         Returns:
#             JsonObject or None: A populated JsonObject instance or None if the request was unsuccessful.
#         """
#         req = requests.get(uri)
#         if req.status_code == 200:
#             if cls is JsonObject:
#                 return cls.load(req.text)
#             else:
#                 return cls.parse(req.text)
#         return None
#
#     def __dataframe_values__(self):
#         """
#         Internal method to prepare data for conversion into a pandas DataFrame.
#         """
#         return [v.to_dataseries(recursive=True) if isinstance(v, JsonObject) else v.to_dataframe(recursive=True) if isinstance(v, JsonList) else v for v in self.get_values()]
#
#     def to_dataseries(self, recursive: bool = False):
#         """
#         Convert the JsonObject into a pandas Series.
#
#         Args:
#             recursive (bool, optional): If True, converts nested JsonObjects and JsonLists as well.
#
#         Returns:
#             pandas.core.series.Series: A pandas Series representation of the JsonObject.
#         """
#         import pandas as pd
#         columns = self.get_columns()
#         if recursive:
#             values = self.__dataframe_values__()
#         else:
#             values = self.get_values()
#
#         return pd.core.series.Series(dict(zip(columns, values)))
#
#     def to_dict(self):
#         """
#         Convert the JsonObject into a standard Python dictionary.
#
#         Returns:
#             dict: A dictionary representation of the JsonObject.
#         """
#         return {a: self[a] for a in self.get_members()}
