import typing
from ..core.type_binding import TypeBinding, JsonTypes, Bindings
from jsonbind.special.serializable import Serializable
from .util import bin_search, SearchType, SortOrder, NotFoundBehavior


class List(list, Serializable):

    def __init__(self, list_type=None, iterable=None, allow_empty: bool = False):
        if list_type is not None:
            if not Bindings.is_bonded(list_type):
                raise TypeError(f"list type {list_type} is not serializable")
        self.list_type = list_type
        self.allow_empty = allow_empty
        list.__init__(self)
        if iterable:
            list.__iadd__(self, map(self.__type_check__, iterable))

    @staticmethod
    def create_type(list_type=None, allow_empty: bool = False, list_name: str = "") -> type:
        def __init__(self, iterable=None):
            List.__init__(self, iterable=iterable, list_type=list_type, allow_empty=allow_empty)
        if not list_name:
            list_name = "%sList" % list_type.__name__
        new_type = type(list_name, (List,), {"__init__": __init__})
        return new_type

    def __type_check__(self, value) -> typing.Any:
        if id(value) == id(self):
            raise ValueError("recursive lists are not allowed")

        if value is None:
            if not self.allow_empty:
                raise TypeError(f"this list does not allow empty values")
            return value


        if self.list_type:
            if not isinstance(value, self.list_type):
                if self.list_type is float and type(value) is int:  # json ints can also be floats
                    value = float(value)
                else:
                    raise TypeError(f"this list only allows values of type {self.list_type.__name__}")
        else:
            if not Bindings.is_bonded(python_type=value.__class__):
                raise TypeError(f"value of type {value.__class__} is not serializable")
        return value

    def __iadd__(self, other):
        list.__iadd__(self, map(self.__type_check__, other))
        return self

    def __add__(self, other):
        new_list = List(list_type=self.list_type, iterable=self)
        new_list.__iadd__(other)
        return new_list

    def __radd__(self, other):
        new_list = List(list_type=self.list_type, iterable=other)
        new_list.__iadd__(self)
        return new_list

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            value = map(self.__type_check__, value)
        else:
            value = self.__type_check__(value)
        list.__setitem__(self, index, value)

    def append(self, value):
        list.append(self, self.__type_check__(value))

    def extend(self, iterable):
        list.extend(self, self.__type_check__(iterable))

    def insert(self, i, value):
        list.insert(self, i, self.__type_check__(value))

    def split_by(self, m: typing.Callable) -> dict:
        result = {}
        for item in self:
            computed_field = m(item)
            if computed_field not in result:
                result[computed_field] = self.__class__()
                self.list_type = self.list_type
            result[computed_field].append(item)
        return result

    def filter(self, key: typing.Any) -> "List":
        filtered_list = self.__class__()
        filtered_list.list_type = self.list_type
        for item in self:
            if key(item):
                filtered_list.append(item)
        return filtered_list

    def find_first(self, key, not_found_behavior=NotFoundBehavior.RaiseError):
        index = self.find_first_index(key, not_found_behavior=not_found_behavior)
        return None if index is None else List.__getitem__(self, index)

    def find_first_index(self, key, not_found_behavior=NotFoundBehavior.RaiseError):
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
        i = bin_search(self, value, key=key, search_type=search_type, order=order, not_found_behavior=not_found_behavior)
        return None if i is None else List.__getitem__(self, i)

    def find_ordered_index(self,
                           value,
                           key=None,
                           search_type: SearchType = SearchType.Exact,
                           order: SortOrder = SortOrder.Ascending,
                           not_found_behavior: NotFoundBehavior = NotFoundBehavior.RaiseError):
        return bin_search(self,
                          value,
                          key=key,
                          search_type=search_type,
                          order=order,
                          not_found_behavior=not_found_behavior)

    def map(self, process: typing.Callable) -> "List":
        new_list = List()
        for item in self:
            new_list.append(process(item))
        return new_list

    def __copy__(self) -> "List":
        return List(list_type=self.list_type, iterable=self)

    def __deepcopy__(self, memo: dict = None) -> "List":
        from copy import deepcopy
        new_list = self.__class__()
        List.__init__(new_list, list_type=self.list_type)
        memo[id(self)] = new_list
        new_list.__iadd__(map(lambda m: deepcopy(m, memo=memo), self))
        return new_list

    def copy(self) -> "List":
        return List.__copy__(self=self)

    def deepcopy(self) -> "List":
        return List.__deepcopy__(self=self)


class ListBinding(TypeBinding):
    def __init__(self):
        super().__init__(json_type=list, python_type=List)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        json_value = self.json_type(map(Bindings.to_json_value, python_value))
        return json_value

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        python_value: List = python_type()
        for item in json_value:
            python_value.append(Bindings.to_python_value(json_value=item, python_type=python_value.list_type))
        return python_value


Bindings.set_binding(ListBinding())


